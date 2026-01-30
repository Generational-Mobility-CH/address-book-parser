# About the project

This ongoing project aims to read, transcribe, and transform the content of historical address books from several Swiss cities into structured household- or individual-level panel datasets. 

The different steps of the pipeline have each their own submodule under `/modules`:
- [Pages Downloader](../modules/pages_downloader/README.md)
- [Pages Preprocessor](../modules/pages_preprocessor/README.md)
- [Text Cleaner](../modules/text_cleaner/README.md)
- [Text Parser](../modules/text_parser/README.md)
- [Text Standardizer](../modules/text_standardizer/README.md)
- [Transcriptor](../modules/transcriptor/README.md)

The resulting dataset is stored as a SQL .db file that looks like the following:
![Output example](assets/screenshot_pipeline_output_1.png)


Steps performed by the pipeline:
1. Download relevant chapters from source websites
2. Preprocess book pages, i.e. cut the pages into single columns for easier further processing
3. Extract the text content of the pages via OCR
4. Process each person's information like the following:
   1. Run a fuzzy match on street names to correct transcription mistakes or LLM hallucinations where possible
      1. where this is not possible, the entry is marked with a TODO tag like "<Todo ...>"
   2. Separate the person's spouse and create a separate entry for them:
   ![Output example](assets/screenshot_pipeline_output_couple.png)
   3. Standardize abbreviations of first names and jobs  
   E.g. see picture above frdr. -> Friedrich; Farbarb. -> Farbarbeiter
   4. Identify a person's gender where possible
      1. The information used to identify a person's gender is noted in the column 'gender_confidence'.  
      The concrete variables used and their weight will be defined at a later stage. 
      So far simple values have been implemented in order to showcase this functionality.      
5. Save the result into a SQL database

## Current Progress
The [Basel address books](https://dls.staatsarchiv.bs.ch/records/hierarchy/1255539?context=%2Frecords%2F1255539) have been successfully processed, demonstrating the pipeline's effectiveness as an initial end-to-end showcase.
The next steps are:
- clean up the database
- requirements engineering with reasearchers needs on panel dataset (will be done after March 2026)
- process the address books of further cities

## Next Steps
The following step has yet to be implemented in order to further develop the panel_dataset:
- Develop a fuzzy-matching algorithm to link individuals across volumes, accounting for changes in surname after marriage as well as possible changes in address or occupation


