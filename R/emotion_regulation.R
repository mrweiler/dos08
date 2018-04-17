##### Import results from Experiment Factory's 
##### emotion regulation and save as csv file

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
    paste0("data/expfactory/", id, "_finished/emotion-regulation-results.json"))

  # extract data table
  tbl <- as_tibble(jsonlite::fromJSON(data_list[[1]][[1]]))
  
  # convert list of "possible_responses" to string
  tbl$possible_responses <- tbl$possible_responses %>%
    as.character() %>%
    str_replace_all("c\\(", "") %>%
    str_replace_all("\\)", "")

  # add tbl to dataset
  dataset <- bind_rows(dataset, tbl)
  
}
  
# save as csv file
write_csv(x = tbl, path = "emotion-regulation-results-all.csv")
