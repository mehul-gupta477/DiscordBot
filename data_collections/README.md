# Data-Collections Documentation

## Purpose

This directory of the project focuses on how data is collected and managed. Data is extracted from various sources using automated scripts via our YAML GitHub Workflows. Once gathered, the data is formatted and stored in `runningCSV.csv`, making it easy for our data-processing sub-team to use.

In this document, you will learn how our data is stored after being extracted from these various sources. This document is mainly for our data-processing sub-team to understand our storage containers.

## RunningCSV Format

Below is how the `runningCSV.csv` file is formatted

| Type | Title | Description | whenDate | pubDate | Location | link | entryDate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Indicator to **separate** the type of career-development item — `Event`, `Job`, or `Internship`. | Title of the event, job, or internship. | Description of the item. | `whenDate`: event date or application deadline. | `pubDate`: original publication date on the source site. | Location of the item. | Link to the item’s page. | `entryDate`: date the item was ingested into the system. |