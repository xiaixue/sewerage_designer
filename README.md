# Sewerage Designer

This program contains different functions useful in the design of a sewerage system

* `asker()` requires the user to input the sections that are going to be analyzed. You can skip this part if you will declare the section within the script, but remember to give them the appropiate format.

  ```
  [
  [Section , Start , End , Lenght , Heigt , Own , Added , Total],
  [Section2 , Start , End , Lenght , Heigt , Own , Added , Total],
  ]
  ```
  And for the manholes.
  ```
  {
    'Start': Elevation,
    'End': Elevation,
  }
  ```
  > **Important**: To stop the input, write 0 and Enter, and if you don't know the accumulated population (Added) write a '**?**'.

  > Sections, starting and ending points can be be strings

  >If you already have the slopes computed, do not execute `slope()` or `exe()`, you will have to manually execute the methods you require.

   _NOTE: All your measurements must be in meters_

---
* `class Sewerage`
  
  This class takes your sections as matrix, and is optional to input additional data. You can specify the $C_s$, $C_d$, $n$, and $dot$.
  
  Where:

  $C_s=security\; factor$

  $C_d = discharge\; coefficient$
  
  $n = rugosity\; coefficient$
  
  $dot = \dfrac{liters/person}{day} $

  **Parameters:** 
    
    * **_tramos_**: _(list)_ List of lists, with the information of each section. For the input format, check `asker()`. 
    * **_pozos_**: _(dictionary)_ Manholes names and elevations.
    * **_cs_**:  _(float)_ Security factor for the design flows. Default set as 1.5
    * **_cd_**:  _(float)_ Discharge coefficient. Default set as 0.8
    * **_dot_**:  _(float)_ Water supply in liters per person per day. Default set as 200
    * **_n_**:  _(float)_ Rugosity based on the material. Default set as 0.009
    * **_cm_**:  _(float)_ Minimum depth of the manhole, measured from the manhole's elevation to the top of the pipe. Default set as 0.9 (meters)

  The class takes as default, $C_d= 0.8$, $C_s= 1.5$, $dot= 200$, and $n= 0.009$ (PVC).
    * `algoFiller()` This function will find and add the corresponding population that comes from other sections and end in incomplete sections where you do not know the total.

      >Input
      ```
      ['A8', '3', '5', 23.4, 0.2 , 100, '?', '?'],
      ['A2', '9', '3', 54.4, 0.5 , 400, 20, 420],
      ```
      >Output
      ```
      ['A8', '3', '5', 23.4, 0.2 , 100, 420, 520],
      ['A2', '9', '3', 54.4, 0.5 , 400, 20, 420],
      ```
      _NOTE: Make sure that your data matches with your project, otherwise the program might fail or return wrong results._
    * `slope()` computes the slopes and elevation difference (heights) of the sections.
    * `designFlows()` computes the minimum, medium, instantaneous and maximum flow of the pipe.
    * `designPrePipe()` does a predesign where it will determine the pipes diameter based merely on the flow rate for the section. Further designing criteria is done on `hydAnalysis()`.
    * `hydAnalysis()` finds the hydraulic depth of the pipe where the, minimum, medium, instantaneous and maximum flow rate happens of each section and does the rest of the designing process.
    * `nivelesArrastre()` finds the bottom level of each manhole. Needed to the determine the real depth of all manholes.

## Designing requirements
  * Pipelines capacity must be greater than the required on the section.
  * Pipelines must be $\le$ 80% filled capacity for the maximum flow rate $Q_{max}$.
  * Minimum slope of 0.002
  * Minimum sections velocity of $0.3 m/s$
***
## Example

> There is sample data to test its functionality.

>>Here there is a small example of the program's function.

![Alt text](/sewer_systemw.png?raw=true "Sewerage System")

For the given data in the picture it should be written as the following.

### Sections data
```
Sec1 A C 80 0.2 50 0 50
Sec2 E G 97 0.2 155 ? ?
Sec3 F G 72 0.1 50 0 50
Sec4 C E 105 0.1 20 ? ?
Sec5 B C 100 0.1 90 0 90
Sec6 D C 45 0.1 40 0 40
```
_**Note** that the name of each section is required and it can be any string. Also the height is not really required, so it doesn't really matter if it is 0.1, 0.2 or -40000._

_Also **Note** that the order is arbitrary._ 

### Manholes data
```
A 2.868
B 2.884
G 2.35
F 2.776
E 2.8
C 3.11
D 3.033
```
Therefore when running the program, it should be done in the following way.
> > Run `sewerage.py`
```
Ingrese sus sus secciones con este formato separadas por un espacio.
Tramo    Inicio  Fin     Longitud        Altura  Propios         Tributarios   Total 
Las poblaciones que no tenga, introdúzcalas con un signo de interrogación (?). 
La altura también puede ponerla como '?'.
Asegúrese de no repetir el nombre de los pozos y preferentemente de los tramos tampoco.
Tramo 1: Sec1 A C 80 0.2 50 0 50
Tramo 2: Sec2 E G 97 0.2 155 ? ?
Tramo 3: Sec3 F G 72 0.1 50 0 50
Tramo 4: Sec4 C E 105 0.1 20 ? ?
Tramo 5: Sec5 B C 100 0.1 90 0 90
Tramo 6: Sec6 D C 45 0.1 40 0 40 
Tramo 7: 0
Ingrese sus la identificación de cada pozo y sus cotas
   Pozo Cota
--> 1: A 2.868
--> 2: B 2.884
--> 3: G 2.35 
--> 4: F 2.776
--> 5: E 2.8  
--> 6: C 3.11 
--> 7: D 3.033
--> 8: 0
```


The output will be a _.xlsx_ file named _sewerage_ with the solution on a calc sheet.

The first sheet will be named _Datos_. Will have only the sections given data. This so the user checks if his input was correct.

| Section | Start | End | Length | Height | Own | Added | Total |
|:-------:|:-----:|:---:|:------:|:------:|:---:|:-----:|:-----:|
|   Sec1  |   A   |  C  |   80   |   0.2  |  50 |   0   |   50  |
|   Sec2  |   E   |  G  |   97   |   0.2  | 155 |   ?   |   ?   |
|   Sec3  |   F   |  G  |   72   |   0.1  |  50 |   0   |   50  |
|   Sec4  |   C   |  E  |   105  |   0.1  |  20 |   ?   |   ?   |
|   Sec5  |   B   |  C  |   100  |   0.1  |  90 |   0   |   90  |
|   Sec6  |   D   |  C  |   45   |   0.1  |  40 |   0   |   40  |

The next sheet will be named _Datos Completos_ where all the results can be checked.

| Section | Start | End | Length | Height | Own | Added | Total | Slope | Harmon Coeff | $Q_{min}$ | $Q_{med}$ | $Q_{inst}$ | $Q_{max}$ | $\varphi$ (in) | $Q_{pipe}$ |
|:-------:|:-----:|:---:|:------:|:------:|:---:|:-----:|:-----:|-------|:------------:|---------|---------|----------|---------|-----------|----------|
|   Sec1  |   A   |  C  |   80   |  -0.16 |  50 |   0   |   50  | 0.002 |      3.8     |    1    |    1    |    3.8   |   4.56  |     8     |   22.1   |
|   Sec2  |   E   |  G  |   97   | -0.148 | 155 |  200  |  355  | 0.002 |      3.8     |    1    |    1    |    3.8   |   4.56  |     8     |   22.1   |
|   Sec3  |   F   |  G  |   72   | -0.426 |  50 |   0   |   50  | 0.005 |      3.8     |    1    |    1    |    3.8   |   4.56  |     8     |   38.01  |
|   Sec4  |   C   |  E  |   105  |  -0.21 |  20 |  180  |  200  | 0.002 |      3.8     |    1    |    1    |    3.8   |   4.56  |     8     |   22.1   |
|   Sec5  |   B   |  C  |   100  | -0.176 |  90 |   0   |   90  | 0.002 |      3.8     |    1    |    1    |    3.8   |   4.56  |     8     |   22.1   |
|   Sec6  |   D   |  C  |   45   | -0.325 |  40 |   0   |   40  | 0.007 |      3.8     |    1    |    1    |    3.8   |   4.56  |     8     |  42.002  |

The next sheet will be named _Analisis Hidraulico_ where the pipe _hydraulic depth_ for corresponding flow rates will be displayed in **centimeters**.

| Section | Start | End |  $y_{min}$  | $y_{med}$ |  $y_{inst}$ |  $y_{max}$  | %$_{filled}$ |  $v_{min}$  |
|:-------:|:-----:|:---:|:-----------:|:----:|:----:|:------:|:------------:|:-----------:|
|   Sec1  |   A   |  C  | 2.94 | 2.94 | 5.70 | 6.26 |  26.19 | 0.677 |
|   Sec2  |   E   |  G  | 2.94 | 2.94 | 5.70 | 6.26 |  26.19 | 0.677 |
|   Sec3  |   F   |  G  | 2.26 | 2.26 | 4.33 | 4.75 |  17.79 |  1.16 |
|   Sec4  |   C   |  E  | 2.94 | 2.94 | 5.70 | 6.26 |  26.19 | 0.677 |
|   Sec5  |   B   |  C  | 2.94 | 2.94 | 5.70 | 6.26 |  26.19 | 0.677 |
|   Sec6  |   D   |  C  | 2.16 | 2.16 | 4.12 | 4.52 |  16.57 | 1.287 |

The next sheet will be named _Niveles de Arrastre Hidraulico_ where manholes elevations and heights will be displayed, also the difference between both numbers which stands for the minimum level of the manhole.

| Manhole | Elevation | Elev-Mheight<br>HydragLevel | Manhole Height |
|:-------:|:---------:|:------------------------:|:--------------:|
|    A    |   2.868   |          1.1648          |     1.7032     |
|    B    |   2.884   |          1.1808          |     1.7032     |
|    G    |    2.35   |          0.6468          |     1.7032     |
|    F    |   2.776   |          1.0728          |     1.7032     |
|    E    |    2.8    |          0.7948          |     2.0052     |
|    C    |    3.11   |          1.0048          |     2.1052     |
|    D    |   3.033   |          1.3298          |     1.7032     |

> The flow rates are in $l/s$
