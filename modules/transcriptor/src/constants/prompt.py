PROMPT = """
Output the text seen in the image.
Replace each long — with the previous last name.
The short - means both last names belong together.
Ignore entries, for which the street name comes before the house number.
The output format is: "last_name"; "partner_last_name"; "first_names"; "gender"; "street_name"; "house_number"; "job"; "original_entry"
Ensure there is info for each of those fields, else write <NONE>. Use only ";" as separator.
Example input:
Müller-Bachmann Heinrich, ...
— -Bailly Petra, ...
Meyer Daniel, ...
— -Bachmann Wwe. Anna, ...
Example output:
Müller; Bachmann; Heinirch; male; Bahnhofstr.; 14; Lehrer; Müller, Bachmann, Heinirch, Bahnhofstr. 14, Lehrer
Müller; Bailly; Petra; female; Bahnhofstr.; 14; Lehrerin; — -Bailly Petra, Bahnhofstr. 14, Lehrerin
Meyer; <NONE>; Daniel; male; Bahnhofstr.; 14; Kaufmann; Meyer Daniel, Bahnhofstr. 14, Kaufmann
Meyer; Bachmann; Wwe. Anna; female; Bahnhofstr.; 14; Lehrerin; — -Bachmann Wwe. Anna, Bahnhofstr. 14, Lehrerin
"""

INPUT_PROMPT = [
    {
        "role": "user",
        "content": [
            {"type": "input_text", "text": f"{PROMPT}"},
            {
                "type": "input_image",
                "image_url": "data:image/jpeg;base64,<REPLACE_WITH_BASE64_IMG>",
            },
        ],
    }
]
