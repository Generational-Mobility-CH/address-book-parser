# Data Models
In the address books, we find the following data about a person:
- Names
  - first names
  - last names
  - partner's last name (if present)
- Job description
- Address
  - street name
  - house number (can also be "1a" etc.)

We also store the following meta-information:
- the year of the address book
- the page number, in which the person was found
- the original entry as it was transcribed

And we add the following information:
- the person's gender
  - and the factors used to determine it
- if a partner's last name is present, we create a separate entry for the partner
- TODO: the coordinates of the address for geo-referencing

In our dataset, we store the person object with these attributes:  
[Person class definition](../modules/shared/models/panel_data_entry.py)
```python
# person's attributes
first_names: str
last_names: str
partner_last_names: Optional[str] = ""
job: str
address=Address(
    street_name=street_name, 
    house_number=house_number
)
gender: str = 'M' | 'F' | 'N/A'
gender_from: Optional[str] = ""
original_names: Optional[str] = ""

# metadata
year: int
pdf_page_number: int
original_entry: str
```