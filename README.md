# Sewerage Designer

 Read this in other languages: [Español](www.google.com), [中文](www.google.com)
***

This program contains different functions useful in the design of a sewerage system

* `asker()` requires the user to input the sections that are going to be analyzed. You can skip this part if you will declare the section within the script, but remember to give them the appropiate format.

  ```
  [Section , Start , End , Lenght , Heigt , Own , Added , Total],
  ```
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
    * `slope()` calculates the slope
    * `designPipe()` computes the minimum, medium, instantaneous and maximum flow of the pipe and designs the pipe with an appropiate diameter for each section.
    * `separationRegulations()` checks the sections that exceed the maximum separation length between manholes based on the diameters given by a predesign and create new sections with new manholes according to the needs.  
      > Do not run if you have well defined lengths of the sections in your project.
    * `hydAnalysis()` finds the hydraulic depth of the pipe where the; minimum, medium, instantaneous and maximum flow happens of each section.
    * `exe()` executes all the methods of the class for matters of practicity. If you have not calculated anything whatsoever, it is recommended to go straight to this method, so everything is done.
   
