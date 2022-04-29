import random, math, scipy.optimize as sci, matplotlib.pyplot as plt, xlsxwriter, sys 
from sample_data import *
def asker():
  sections, pozos = list(), list()
  print('Ingrese sus sus secciones con este formato separadas por un espacio.')
  print('Tramo\t Inicio\t Fin\t Longitud\t Altura\t Propios\t Tributarios\t Total \nLas poblaciones que no tenga, introdúzcalas con un signo de interrogación (?). \nLa altura también puede ponerla como \'?\'.\nAsegúrese de no repetir el nombre de los pozos y preferentemente de los tramos tampoco.')
  count = 1
  while True:
    ans = input(f'Tramo {count}: ')
    count += 1
    if ans == '0' or ans == 'salir': break
    elif ans == '': count -= 1
    else:
      ans = ans.split()
      sections.append(ans)

  print("Ingrese sus la identificación de cada pozo y sus cotas")
  count = 1
  print("   Pozo\tCota")
  while True:
    ans = input(f'--> {count}: ')
    count += 1
    if ans == '0' or ans == 'salir': break
    elif ans == '': count -= 1
    else:
      ans = ans.split()
      pozos.append(ans)

  for section in sections:
    index = 3
    for dato in section[3:]:
      try:
        dato = float(dato)
        section[index] = dato
      except: pass
      finally: index += 1

  pozos_dict = dict()
  for pozo in pozos:
    pozos_dict[pozo[0]] = float(pozo[1])

  return sections, pozos_dict

#[ Nom , PI , PF , length , height , own , added , total , slope , harmon , Qmin , Qmed , Qinst , Qextr, diameter, Qpipe ]
#[ 0   , 1  , 2  ,   3    ,  4     ,  5  ,   6   ,   7   ,   8   ,   9    ,  10  ,  11  ,   12  , 13   ,        14    ,  15   ]

class Sewerage:
  def __init__(self, tramos, pozos, cs = 1.5, cd = 0.8, dot = 200, n = 0.009):
    self.pozos, self.tramos = pozos, tramos
    # Settings
    self.cs, self.cd, self.dot, self.n = cs, cd, dot, n 

    # Defining the PreNAH of all the manholes
    self.pre_nah = dict()
    for x, h in self.pozos.items():
      self.pre_nah[x] = h - 0.5

  def algoFiller(self):
    sections_goodie = list()
    sections_baddie = list()

    for i in self.tramos:
      i = list(i)
      if type(i[6]) != type('?'): sections_goodie.append(i)
      else: sections_baddie.append(i)

    if len(sections_baddie) == 0:
      return self.tramos

    while True:
      ran = random.choice(sections_baddie)
      start = ran[1]
      total = 0

      for h in self.tramos:

        if h[2] == start:
          if h[7] == '?':
            self.tramos = sections_baddie + sections_goodie
            return self.algoFiller()
          else:
            total += h[7]
            continue
        else: continue
      else: break

    add = total
    sections_baddie.remove(ran)
    ran[6] = add
    ran[7] = ran[6] + ran[5]
    sections_goodie.append(ran)

    if len(sections_baddie) != 0:
      self.tramos = sections_baddie + sections_goodie
      return self.algoFiller()
    else:
      self.tramos = sections_goodie
      return self.tramos

  def slope(self):
    for i in self.tramos:
      # Calculate/Confirm the height
      difference = self.pozos[i[1]] - self.pozos[i[2]]
      i[4] = round( abs( difference ), 3)

      # Calculate Slopes
      slope = i[4] / i[3]
      if slope < 0.002:
        i.append(0.002)
      elif difference <= 0:
        i.append(0.002)
      else:
        i.append(slope)
    return self.tramos

  def designPipe(self, dtfix = set()):
    for h, i in enumerate(self.tramos):
      # Checker #
      index = set()
      index.add(h)
      if len(i) > 9:
        d = i[14]
        del i[9:]
      else: 
        pass
      
      #	Harmon Coeff #
      if i[7] < 1000: M = 3.8
      elif i[7] > 63450: M = 2.7
      else: M = 1 + 14 / ( 4 + math.sqrt( i[7] / 1000 ) )
      i.append(M)

      # Flows #
      q_med = self.dot * self.cd * i[7] / 86400
      if q_med < 1: q_med = 1
      else: q_med += 0

      q_min = q_med * 0.5

      if q_min < 1: q_min = 1
      else: q_min += 0

      q_inst = q_med * M
      q_extr = q_inst * self.cs
      i.append(q_min)
      i.append(q_med)
      i.append(q_inst)
      i.append(q_extr)

      diameter = 8
      # Design Tube #
      q_full = lambda diam: (1 / self.n) * (i[8] ** (1/2)) * ((diam/4) ** (2/3)) * 1000 * math.pi * (diam ** 2) / 4

      if index.issubset(dtfix) == False: 
        while True:
          phi = diameter * 0.0254
          q_comp = q_full(phi)
          if q_comp > q_extr:
            i.append(diameter)
            i.append(q_comp)
            break
          else:
            diameter += 2
            continue
      else:
        d += 2
        q_comp = q_full(d)
        i.append(d)
        i.append(q_comp)
      
    if len(dtfix) != 0:
      return self.hydAnalysis()
    return self.tramos

  def hydAnalysis(self):
    self.analysis = list()
    bad_indexes = set()

    for z, i in enumerate(self.tramos):
      tramo = list()
      d = i[14] * 0.0254
      r = d / 2
      s = i[8]
      flows = [ i[10], i[11], i[12], i[13] ]

      tramo.append(i[0])
      tramo.append(i[1])
      tramo.append(i[2])

      area = lambda theta: ( math.pi * theta / 360 - 0.5 * math.sin( math.radians(theta) ) ) * ( r ** 2 )
      rh = lambda theta: ( 1 - 360 * ( math.sin( math.radians(theta) ) / theta / math.pi / 2) ) * r / 2
      velocity = lambda theta: ( 1 / self.n ) * ( rh(theta) ** (2 / 3) ) * ( s ** (1 / 2) )
      t = lambda theta: r * ( 1 - math.cos( math.radians( 0.5 * theta ) ) ) * 100
      flowCompute = lambda angle, flow: area(angle) * velocity(angle) * 1000 - flow

      for u in flows:
        phi = sci.bisect(flowCompute, 0.0001, 360, args=(u))
        tirante = t(phi)
        tramo.append(tirante)
      
      prctg_filled = area(phi) * 100 / area(360)
      tramo.append(prctg_filled)

      if prctg_filled >= 80:
        bad_indexes.add(z)
  
      self.analysis.append(tramo)

    if len(bad_indexes) == 0:
      return self.analysis
    else:
      return self.designPipe(dtfix = bad_indexes)

  def nivelesArrastre(self):
    self.new_nah = self.pre_nah

    for i in self.tramos:
      start, end, slope, lenght = i[1], i[2], i[8], i[3]
      if self.pre_nah[end] < self.pre_nah[start]:
        self.new_nah[start] = self.pre_nah[start]
        self.new_nah[end] = self.pre_nah[end]
        continue
      else:
        self.new_nah[start] = self.pre_nah[start]
        self.new_nah[end] = self.pre_nah[start] - slope * lenght

    if self.new_nah == self.pre_nah:
      return self.new_nah
    else:
      return self.nivelesArrastre()


if __name__ == '__main__':
  "Add Velocity check, read excel"
  # section, manholes = asker()  
  sew = Sewerage(section, manholes, n= 0.01)
  sys.setrecursionlimit(10000); 
  filled = sew.algoFiller()
  
  slopes = sew.slope()
  design = sew.designPipe()
  nah    = sew.nivelesArrastre()
  hyd    = sew.hydAnalysis()

  workbook = xlsxwriter.Workbook("sewerage.xlsx")
  data_inc  = workbook.add_worksheet('Datos')
  data_cmp  = workbook.add_worksheet('Datos Completos')
  analysis  = workbook.add_worksheet('Analisis Hidraulico ')
  pozosnivl = workbook.add_worksheet('Niveles de Arrastre Hidraulico')

  def writtingExcel(data, wksheet):
    format = workbook.add_format()
    format.set_align('center')
    format.set_align('vcenter')
    format.set_font_name('Open Sans')
    format.set_font_size(12)
    if type(data) != type({'s': 3}):
      row = 0
      for x in data:
        col = 0
        for y in x:
          wksheet.write(row,col, y, format)
          col += 1
        row += 1
    else:
      row = 0
      for x, y in data.items():
        wksheet.write(row, 0, x, format)
        wksheet.write(row, 1, sew.pozos[x], format)
        wksheet.write(row, 2, y, format)
        if y < 0: wksheet.write(row, 3, sew.pozos[x] + y * -1, format)
        else: wksheet.write(row, 3, sew.pozos[x] - y, format)
        row += 1
    return 0

  writtingExcel(section, data_inc)
  writtingExcel(sew.tramos, data_cmp)
  writtingExcel(hyd, analysis)
  writtingExcel(nah, pozosnivl)
  
  workbook.close()

  for shit in sew.tramos:
    if shit[1] == '71':
      a = shit
      break
  memory_mh = list()
  memory_mh.append(a[1])
  memory_mh.append(a[2])

  def getter(tramo, mh):
    end = tramo[2]      
    while True:
      rnd_section = random.choice(sew.tramos)
      if end == rnd_section[1]:
        mh.append(rnd_section[2])
        return getter(rnd_section, mh)
      if end == '26':
        break
    return mh
  
  omg = getter(a, memory_mh)
  nivpzo, nivnah = list(), list()
  for j in omg:
    nivpzo.append(sew.pozos[j])
    nivnah.append(sew.new_nah[j])
  print(omg)
  print(nivnah)
  print(nivpzo)

  plt.plot(omg, nivnah, '-.c', label= 'Nivel de Arrastre Hidráulico')
  plt.plot(omg, nivpzo, '-m', label= 'Nivel del Rasante')
  plt.legend()
  plt.show()

"""
  order = dict()

  for h, i in enumerate(sections_goodie):
    order[i[0]] = h
  
  new_order = list(order)
  new_order.sort()
  ordered_sections = list()
  
  for x, y in enumerate(new_order):
    section_index = order[y]; section = sections_goodie[section_index]
    ordered_sections.append(section)
"""
