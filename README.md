# COMP 370 Homework 4 - 311 Data Analysis

## Task 0.5 Trim dataset and add headers

To only get data from 2020

```shell
grep -P "^\d{8,10},\d{2}/\d{2}/2020" <data> > output.csv
```

Add headers to csv file

```shell
cat headers.csv > <newfile> && cat output.csv >> <newfile>
```

