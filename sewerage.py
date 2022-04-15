import random, math

def asker():
  sections = []
  print('Ingrese sus sus secciones con este formato separadas por un espacio.')
  print('Tramo\t Inicio\t Fin\t Longitud\t Altura\t Propios\t Tributarios\t Total \nLas poblaciones que no tenga, introdúzcalas con un signo de interrogación (?).')
  count = 1
  while True:
    ans = input(f'Tramo {count}: ')
    count += 1
    if ans == '0' or ans == 'salir': break
    elif ans == '': count -= 1
    else: 
      ans = ans.split()
      sections.append(ans)

  for section in sections:
    index = 3
    for dato in section[3:]:
      try:
        dato = float(dato)
        section[index] = dato
      except: pass
      finally: index += 1
  return sections

#[ Nom , PI , PF , 60 , 3 , own , added , total , slope , harmon , Qmin , Qmed , Qinst , Qextr, diameter, Qpipe ]
#[ 0   , 1 , 2 ,   3  , 4 ,  5  ,   6   ,   7   ,   8   ,   9    ,  10  ,  11  ,   12  , 13   ,    14   ,  15   ]

class Sewerage:
  def __init__(self, tramos, **data):
    self.tramos = tramos
    for x, y in data.items():
      if x == 'cs' : self.cs  = y
      if x == 'cd' : self.cd  = y
      if x == 'dot': self.dot = y
      if x == 'n'  : self.n   = y
    try:    self.cs += 0
    except: self.cs = 1.5
    try:    self.cd += 0
    except: self.cd = 0.8
    try:    self.dot += 0
    except: self.dot = 200
    try:    self.n += 0
    except: self.n = 0.009

  def algoFiller(self):
    sections_goodie = list()
    sections_baddie = list()

    for i in self.tramos:
      i = list(i)
      if i[6] != '?': sections_goodie.append(i)
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
      slope = i[4] / i[3]
      i.append(slope)
    return self.tramos

  def designPipe(self):
    for i in self.tramos:
      # Checker #
      if len(i) > 9: del i[9:]
      else: pass

      #	Harmon Coeff #
      if i[7] < 1000: M = 3.8
      elif i[7] > 100000: M = 2
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
      while True:
        phi = diameter * 0.0254
        q_init = (1 / self.n) * (i[8] ** (1/2)) * ((phi/4) ** (2/3)) * 1000 * math.pi * (phi ** 2) / 4
        if q_init > q_extr:
          i.append(diameter)
          i.append(q_init)
          break
        else:
          diameter += 2
          continue
    return self.tramos

  def separationRegulations(self):
    wrong = list()
    fixed = list()

    for i in self.tramos:
      d = i[14] * 2.54

      if d < 61: s = 100
      elif 61 <= d < 122: s = 125
      elif 122 <= d < 305: s = 150
      else: s = 150

      if i[3] > s:
        divider = int( round(i[3] / s, 0) )
        incorrect = ( i , math.ceil(i[3] / s) )
        wrong.append(incorrect)
      else: continue

    for x in wrong:
      # Assigning values #
      h = x[1]
      partial = x[0]

      # Properties #
      new_lenght = partial[3] / ( h )
      start = str(partial[1])
      section = partial[0]
      own = partial[5] / h
      added = partial[6]

      for i in range(1,h+1):
        section_fine = list()
        section_fine.append(section)
        section_fine.append(start)

        if i == h: start = partial[2]
        else: start += "'"

        section_fine.append(start)
        section_fine.append(new_lenght)
        section_fine.append(partial[4])
        section_fine.append(own)
        section_fine.append(added)
        section_fine.append(own + added)
        section_fine.append(partial[8])
        added += own
    
        fixed.append(section_fine)
    for k in wrong:
      self.tramos.remove(k[0])
    self.tramos += fixed
    
    return self.designPipe()

  def hydAnalysis(self):
    self.analysis = list()
    for i in self.tramos:
      tramo = list()
      d = i[14] * 0.0254
      r = d / 2
      s = i[8]
      q_min, q_med, q_int, q_ext = i[10], i[11], i[12], i[13]
      theta_deg = 0

      tramo.append(i[0])
      tramo.append(i[1])
      tramo.append(i[2])

      area     = lambda theta: ( math.pi * theta / 360 - 0.5 * math.sin( math.radians(theta) ) ) * ( r ** 2 )
      rh       = lambda theta: ( 1 - 360 * ( math.sin( math.radians(theta) ) / theta / math.pi / 2) ) * r / 2
      velocity = lambda theta: ( 1 / self.n ) * ( rh(theta) ** (2 / 3) ) * ( s ** (1 / 2) )
      theta    = lambda depth: 2 * math.acos( ( 1 - ( depth / r ) )*( math.pi / 180 ) )
      tirante  = lambda theta: r * ( 1 - math.cos( math.radians( 0.5 * theta ) ) ) * 100

      error = 100
      while True:
        theta_deg += 0.001
        q_comp = area(theta_deg) * velocity(theta_deg) * 1000
        error = abs(q_min - q_comp) * 100 / q_min
        t = tirante(theta_deg)
        if error < 1:
          break
        else: continue
      tramo.append(t)
      
      error = 100
      while True:
        theta_deg += 0.001
        q_comp = area(theta_deg) * velocity(theta_deg) * 1000
        error = abs(q_med - q_comp) * 100 / q_med
        t = tirante(theta_deg)
        if error < 1:
          break
        else: continue
      tramo.append(t)

      error = 100
      while True:
        theta_deg += 0.001
        q_comp = area(theta_deg) * velocity(theta_deg) * 1000
        error = abs(q_int - q_comp) * 100 / q_int
        t = tirante(theta_deg)
        if error < 1:
          break
        else: continue
      tramo.append(t)

      error = 100
      while True:
        theta_deg += 0.001
        q_comp = area(theta_deg) * velocity(theta_deg) * 1000
        error = abs(q_ext - q_comp) * 100 / q_ext
        t = tirante(theta_deg)
        if error < 1:
          break
        else: continue
      tramo.append(t)
      self.analysis.append(tramo)
    return self.analysis
  
  def exe(self):
    self.algoFiller()
    self.slope()
    self.designPipe()
    self.separationRegulations()
    return self.tramos

if __name__ == '__main__':
  analysis = asker()
  sew = Sewerage(analysis, cd = 0.8, cs= 1.5,dot= 200 ,n= 0.009)
  for i in sew.exe():
    print(i)
  for i in sew.hydAnalysis():
    print(i)