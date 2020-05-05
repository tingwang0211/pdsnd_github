Notes to the instructor:

1. On separating getting user inputs on city, moth and day of the week into two functions (get_city() and get_filters()):
The city name is used to load the data file of one particular city into a DataFrame, which takes the most amount of execution time..
Based on my understanding, normally a user would like to explore the statistics of one particular city in a different way before switching to a different city to study (for e.g. the user may want to look at the statistics on a weekday in June after he/she had seen relevant statistics on Sundays in June for comparison.). get_filters() gets the month and day of the week for filtering, which allows the user to examine the data of one city in multiple different ways before switching to a different city - thus reduces the need of data reloading while still maximizes the data exploration experiences.

2. On time display (for #3 Trip duration)
The original trip duration was recorded in seconds, which isn't intuitive at all to be displayed directly to the users (for e.g. if no filter is applied, the total travel time is about 300 million seconds). Although the timedelta function can help to convert the time duration into a relatively more readable format: XXX Days, HH:MM:SS, I personally still think it is easier for general users to see a time duration in the XXX Days, HH Hour(s), MM Minute(s), SS Second(s) format.
