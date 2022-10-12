# HAC-webpage

A website made from Flask that retrieves grades from Home Access Center (A common grade adiministration system in Texas K-12 public schools)
***
## Features

* Grade retreival (basically the same as using HAC)
* Final grade calculator
* Simulated Grades
* Max/Min Grade calculator

## Setup

Install dependent modules from `requirements.txt` and the run the file `run.py`

## Usage

**Front page**
> Log into HAC through the login form <br>
> Final Grade calculator that takes in current grade, weight of final, and target grade.

**All Grades Page**
> Displays grades from every class <br>
> The title gives the name of the class as well as the rounded average (rounded to a whole number) <br>
> The format for each class is <br>
> |Title|Date|Credit|Total|Grade|Type|
> |-|-|-|-|-|-|
> |Title of the class|Date Due|Points Given|Total Points|Percentage:  $$\frac{Credit}{Total}$$|Grade Bracket (Major/Minor/Midterm/Final)| 
>
> Additionally, each class displays the aggregate grades for each grade bracket in
> |Type|Points|Total|Percent|Weight|Credit|
> |-|-|-|-|-|-|
> |Grade Bracket (Major/Minor/Midterm/Final)|Points Given|Total Points|Percentage:  $$\frac{Points}{Total}$$|Weight of the Grade Bracket out of 100|Points given that will be summed to form the final grade| 

**Class Page**

> Similar to the `All Grades Page` The class page displays course information in the same way <br><br>
> It also provides Extra Grade Tools <br><br>
> **Add Grade** <br>
> Simulates the addition of a grade (out of 100) in a given Grade Bracket <br><br>
> **Grade Goal** <br>
> Visually adds grades to the course information display to show the user the maximum or minimum grade needed for a target grade goal<br><br>
> e.g. Target grade is 97, which will require 2 100% on Minor Grades and 1 98% on a Minor Grade <br>
> e.g. Target grade is 70, which will require at least a 62% on the next Test (Major Grade)
***
> *Does store login information