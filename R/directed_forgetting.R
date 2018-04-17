##### Import results from Experiment Factory's 
##### directed-forgetting and save as csv file

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
  # import file
  data_list <- read_json(
    paste0("data/expfactory/", id, "_finished/directed-forgetting-results.json"))
  
  # convert list to tibble
  tbl <- as_tibble(jsonlite::fromJSON(data_list[[1]][[1]]))
  
  # convert list of "block_duration" to string
  tbl$block_duration <- tbl$block_duration %>%
    str_replace_all("NULL", "NA") %>%
    unlist()
  
  # convert list of "possible_responses" to string
  tbl$possible_responses <- tbl$possible_responses %>%
    as.character() %>%
    str_replace_all("list\\(", "") %>%
    str_replace_all("c\\(", "") %>%
    str_replace_all("\\)", "")
  
  # convert list of "stim_top" to string
  tbl$stim_top <- tbl$stim_top %>%
    as.character() %>%
    str_replace_all("c\\(", "") %>%
    str_replace_all("\\)", "")
  
  # convert list of "stim_bottom" to string
  tbl$stim_bottom <- tbl$stim_bottom %>%
    as.character() %>%
    str_replace_all("c\\(", "") %>%
    str_replace_all("\\)", "")
  
  # add subject id
  tbl <- tbl %>%
    mutate(id = id)
  
  # reorder columns
  tbl <- tbl %>%
    select(id, everything())

  # add tbl to dataset
  dataset <- bind_rows(dataset, tbl)

}

# save as csv file
write_csv(x = dataset, path = "directed-forgetting-results-all.csv")
