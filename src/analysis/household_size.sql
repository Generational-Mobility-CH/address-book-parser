SELECT
    COUNT(*) AS NumberOfPersons,
    street_name,
    house_number,
    CONCAT(first_names,' ', last_names, ' ', partner_last_names) AS Names,
    year
FROM
    persons
WHERE
    street_name NOT LIKE '<Keine Angabe Gefunden>'
    AND street_name NOT LIKE ''
    AND house_number NOT LIKE '<Keine Angabe Gefunden>'
    AND house_number NOT LIKE ''
GROUP BY
    street_name,
    house_number,
    year
HAVING
    COUNT(*) > 2
ORDER BY
    NumberOfPersons DESC;