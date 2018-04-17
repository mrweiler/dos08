##### Import results from Experiment Factory's 
##### simple-reaction-time and save as csv file

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
    paste0("data/expfactory/", id, "_finished/simple-reaction-time-results.json"))
  
  # convert list to tibble
  tbl <- as_tibble(jsonlite::fromJSON(data_list[[1]][[1]]))
  
  # convert list of "possible_responses" to string
  tbl$possible_responses <- tbl$possible_responses %>%
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
write_csv(x = dataset, path = "simple-reaction-time-results-all.csv")
