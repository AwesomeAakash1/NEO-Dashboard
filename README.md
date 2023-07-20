# NEO-Dashboard

This project is a dashboard that provides key statistics and data visualizations about Near Earth Objects, which are asteroids or comets that pass close to the Earth's orbit. The data used for the dashboard was gathered from NASA's datasets. The dashboard also has filters for the specific objects and rarities that the user wants to view.

## Frameworks

Streamlit was used to create the web app / dashboard.
Pandas was used for data manipulation and the DataFrame, a key data structure used in the project.
Plotly was used for creating custom data visualizations.
Numerize was used to add large statistics in a readable format.
FeedParser is an RSS library used to extract information from the NASA CNEOS blog in order to create an aggregated news feed with important headlines about Near Earth Objects as well as meteorites.


## How to Run

To run this project, copy the files into a Pytohn-compatible IDE. Then, in the terminal, run the following command: "streamlit run main.py". Once you have run the command, copy the link that is displayed into a search engine. From there, interact with the dashboard!

## Layout

The basic layout of the dashboard is three headers and a sidebar. The sidebar contains various filters for viewing the data in a concise manner. The data visualizations are contained in 2 rows of 2 columns. At the bottom of the dashboard, there is an aggregated NEO news feed, which sources relevant headlines from an RSS feed.

## Future Implementations
In the future, I hope to host the NEO Dashboard on a website or server to make it easier to view. I also hope to add more data as well as complex data visualizations that provide more information about NEOs. Additionally, I wish to create a similar dashboard that provides important stats and data viz about exo-planets.

## Image Attributions - Flaticon
###Asteroid icons created by Good Ware
https://www.flaticon.com/free-icons/asteroid

### Diameter icons created by Freepik
https://www.flaticon.com/free-icons/diameter

### Speedometer/Dashboard icons created by Vectors Market
https://www.flaticon.com/free-icons/dashboard

### Infinity icons created by kmg design
https://www.flaticon.com/free-icons/infinity
