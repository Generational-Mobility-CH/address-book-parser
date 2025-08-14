# Module Description

**Main Goal:** To represent the information contained in the address books as truthfully as possible in a 1:1 manner.

**General**
  - Text cleaning.
  - Cleaning up hallucinations.
  - Clean separation of information: name, job, address.
  - Properly filter out lines that do not represent individuals (companies, schools, etc.).

**Detailed**:

- **Names**
  - Replace hyphens with the correct last name.
  - Save the person's names as 1 single field (containing first- and last-names).
  
- **Job**
  - Keep the job titles as they are.
  - Focus on separating the job from the address where there is no comma inbetween.
  
- **Address Parsing**
  - Spellcheck (fuzzy matching) remains in the module.
  - Standardization of street names remains (e.g., Bahnhofstr. -> Bahnhofstrasse).  

💡 Note: These address-handling-related tasks would be more fitting for the 'panel-data' module, but they are kept in this module for time efficiency reasons (the spellchecking of the street names is a very time-consuming task (due to the used fuzzy matching library) that has to be done only once.
