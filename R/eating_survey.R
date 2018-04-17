##### Import results from Experiment Factory's 
##### eating-survey and save as csv file

# load libraries
library(jsonlite)
library(stringr)
library(tidyverse)

# get IDs
id_list <- list.dirs(
  path = "data/expfactory",
  full.names = FALSE) %>%
  str_subset("_finished") %>%
  str_remove_all("_finished")

# create empty tibble
dataset <- tibble()

for (id in id_list) {
  
  # import json file
  data_list <- read_json(
    paste0("data/expfactory/", id, "_finished/eating-survey-results.json"))
  
  # convert list to tibble
  tbl <- as_tibble(data_list)
  
  # move variable names into one column and values into another
  tbl <- gather(tbl, key = varname, value = value)
  
  # edit variable names in column 1
  tbl$varname <- tbl$varname %>%
    str_remove_all(pattern = "data") %>%
    str_remove_all(pattern = "\\[") %>%
    str_remove_all(pattern = "\\]")
  
  # separate question number and variable name
  tbl <- tbl %>%
    extract(varname, c("question_num", "varname"), "([0-9]+)([a-z].*)")
  
  # move variables from varname to separate columns
  tbl <- tbl %>%
    spread(varname, value)
  
  # add subject id
  tbl <- tbl %>%
    mutate(id = id)
  
  # reorder columns
  tbl <- tbl %>%
    select(id, question_num, name, text, options, value)
  
  # sort rows by question number
  tbl$question_num <- as.integer(tbl$question_num)
  tbl <- tbl %>%
    arrange(question_num)
  
  # add tbl to dataset
  dataset <- bind_rows(dataset, tbl)
  
}

# save as csv file
write_csv(x = tbl, path = "eating-survey-results-all.csv")
