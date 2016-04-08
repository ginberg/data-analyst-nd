---
title: "README"
output: html_document
---

###Summary
I analyzed the delays of airlines over the years 2007 until 2016 per carrier. Using the total delay time for a year, the relative delay for airlines can be calculated and airlines 
can be compared. Southwest Airlines is consistenly one of the airlines with the highest delay for these years.

I have downloaded the data from <http://www.transtats.bts.gov/ot_delay/OT_DelayCause1.asp?pn=1>

###Design
I gathered the delay data for each year and for all airlines. I aggregated the delays (in minutes) by airline and year. After that I have calculated the total delay for a year and the delay percentage for each airline. Please refer to project6.R to see the code I have used to create the final dataset.

The airline is a categorical feature in the dataset while the relative delay is a numeric feature. To compare the delays between airlines, I have chosen to use a bar plot, since the size of the delay can be indicated by bar length and it is easy to compare delays in this way. The tooltip of this bar plot gives the exact percentage and the name of the carrier.

To be able to scroll through the time, I have used a bar plot on the left of the main plot. The length of the bar indicates the total delay time for that year. The number in the bar
indicates the year. Each bar (year) is clickable and the delay bar plot is updated with results of that year. When the page is loaded, an animation is started which loops through the years.

###Feedback

####Praveen:
Hi ger, The visualization looks great with right choice of the graph to show the relationship. The units in the Y-axis can be shown . The links in the left side for each year can be changed to hand-pointer cursor to make it more explicit.

####Ritu
Hi Ger,

The visualization looks great. Couple things to address are:

The X and Y axis labels look like they are column names. You can rename them to describe the column with units.
For some carriers the tooltip that shows the airline name is not popping up. Instead the default tooltip shows the column names and values.
When I scroll to the right to see all the carriers. the graph moves into the legend area for the delay type. Not sure if you can find a way to change the scrolling so that does not happen. Also I noticed that the graph and the title scroll to the right, but your header text does not scroll to the write and, on my screen at least, the header text is flowing off the screen on the write to I miss parts of a word(s).

####vivekyadav
What do you notice in the visualization? Graphs show trends of delay for various carriers.

What questions do you have about the data?

What factors contribute to delays in each carrier.
Do reasons of delay vary by airline carrier, also are relative trends of delay similar for different carriers.
Feedback: -It would be nicer if you can provide some description of what the carrier's values on x-axis mean.

When the page loads, the graph is too big to fit in one page.
The values displayed on bar (after tooltip) in some cases appear behind the bars.
The location of x-axis variables change when you change the type of delay, this makes it difficult to compare delays for a particular airline.
It may be helpful to show 2 stacked bar, that way you can see type of delay by carrier, and percentage of type of delay in each carrier.
When you click on the link RITA - - -, the link appears on the same tab as the visualization. You can make it appear in new page by using target = blank in href.
The values on y-axis are not clear. It says "late_aircraft_delay.pct", however, on explanation on bottim it says sum of delays. Am assuming you normalized the values by total delays.

####Changes after feedback
I have made quite a few changes after the feedback. Here is the list:

* plot was too big for some reviewers (didn't fit in one page). I have changed the size of the plot smaller and tested if the plot still looked allright when zooming in and out
in chrome and firefox.
* changed tooltip to use the default one of dimplejs, which prints the text next to the bar.
* changed the ordering of airlines from delay size to carrier. In this way the difference in delay over time is easier to see.
* add x,y labels and units on y axis
* moved the RITA link to README, since it is background information that is not directly relevant in the plot
 
### Used resources
http://www.d3js.org/
http://www.dimplejs.org/
http://www.udacity.com/
http://www.stackoverflow.com/
http://www.rita.dot.gov/bts/help/aviation/html/understanding.html

