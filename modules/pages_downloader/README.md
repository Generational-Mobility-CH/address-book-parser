# Module Description

**Main Goal:** To download the pdfs from Basel's city archive

**General**
  - Scraping through the archive's hierarchy to retrieve the links to the corresponding child-records.
  - Extracting the table of content (toc) of each book from the preview page to retrieve the chapters.
  - If necessary: render the pdfs before download.
  - Download the pdfs of each book.

**Detailed**:

- **Overview and book urls**
  - Basel's address books are organized in subgroups (~20 addressbooks for each subgroup).
  - Start point: 4 urls of the subgroups.
  - Retrieve the book urls from the child-records of each subgroup.
  
- **Table of contents**
  - Each preview page of the book contains a table of content (html)
  - Retrieve the table of content of each book and save it in a separate json file.
  
- **Download and rendering**
  - Scrape through the preview page to retrieve the book id and generate the download url.
  - Download each book using the direct download link.
  - Careful: if download fails, it is likely due to updates to the archive's website, meaning the PDF must be rendered before downloading
  - --> if this is the case, run the rendering function
  - --> if rendering fails, it is likely due to updates to the archive's website and the rendering function must me adapted accordingly (e.g. new button names, new pop-up messages, new content hierarchies)

💡 Note: Page rendering and download is a rather slow process, thus we provide a working example with only one book
