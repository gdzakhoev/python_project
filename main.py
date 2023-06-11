import time
import streamlit as st
import pandas as pd

st.title('Suicide in US states. Survey highlights.')
st.header("About")
st.write('Suicide is an important social problem that requires investigation ' \
         + 'of various aspects. In this study, we will try to analyze some ' \
         + 'classical and philistine sociological (theory of human life value' \
         + '), economic (suicide as an inability to feed oneself), ' \
         + 'physiological (suicide caused by depression associated with ' \
         + 'vitamin D deficiency) theories of suicide as a social phenomenon.' \
         + 'In this study, the emphasis is not on individual factors, but on ' \
         + 'structural determinants. That is, the research question is not ' \
         + '"Why did a person commit suicide?", but "Why is suicide common ' \
         + 'in this region?".')

st.write('We used different demographic data for the 50 US states. ' \
         + 'In some cases where we were not able to fit data for 2020 ' \
         + '(as was the case with religions and the political landscape), ' \
         + 'data were taken for the coming years. More about this in the ' \
         + 'part of the project devoted to self-criticism.')

st.header('Scrapping')
st.code(
"""
# Scrapping political ideology values from pewsearch.org
driver.get(politicalURL)
driver.find_element(
    By.CSS_SELECTOR, 
    '[data-tab="51e56cc7e934ca51e586f1f045786c39-table"]'
).click()
time.sleep(2)

tableDataRaw = driver.find_element(By.TAG_NAME, 'tbody') \\
    .find_elements(By.TAG_NAME, 'tr')

for tableRow in tableDataRaw:
    curColumn = tableRow.find_elements(By.TAG_NAME, 'td')
    
    if len(curColumn) == 0:
        continue

    # Check if the data is state-wide and not country-wide
    stateName = curColumn[0].text

    if stateName not in statesFullList:
        continue

    politicalRateDict['conservative_rate'] \\
        .append((
            stateName,
            percent_to_float(curColumn[1].text)
        ))
    politicalRateDict['moderate_rate'] \\
        .append((
            stateName,
            percent_to_float(curColumn[2].text)
        ))
    politicalRateDict['liberal_rate'] \\
        .append((
            stateName,
            percent_to_float(curColumn[3].text)
        ))
    politicalRateDict['neutral_rate'] \\
        .append((
            stateName,
            percent_to_float(curColumn[4].text)
        ))


politicalRateDict['conservative_rate'] = \\
    [rate for (state,rate) in sorted(politicalRateDict['conservative_rate'])]
politicalRateDict['moderate_rate'] = \\
    [rate for (state,rate) in sorted(politicalRateDict['moderate_rate'])]
politicalRateDict['liberal_rate'] = \\
    [rate for (state,rate) in sorted(politicalRateDict['liberal_rate'])]
politicalRateDict['neutral_rate'] = \\
    [rate for (state,rate) in sorted(politicalRateDict['neutral_rate'])]

# Finally getting political rate DataFrame
politicalRate = pd.DataFrame(data=politicalRateDict).set_index('state')
print(politicalRate)
"""
)

st.write(
    'We skip the scraping stage, which is fully reflected in the notebook.'
)



st.header("Our main table")
statesData = pd.read_csv('EXPstateData.csv')
st.dataframe(statesData)

st.header(
    'Friedman statistical test to see if the state ' \
    + 'difference is statistically significant.'
)
st.code(
"""
f, p = stats.friedmanchisquare(*np.array(stateData.values).T)
print ('Yes' if p < 0.005 else 'No')
# -> Yes
"""
)

st.header("Correlation")
st.write(
    'We tested the extreme case of Alaska. Its area is so large ' \
    + 'that it can litter the data. Does it interfere? At the same ' \
    + 'time, let\'s check our analyze_this function, which displays a ' \
    + 'summary for a specific relationship between two variables.'
)
st.code(
"""
analyze_this('area')
# -> Area summary:
# -> Correlation coefficient is 0.4452
# -> Determination coefficient is 0.1982
# -> P-value is 0.0012
# -> Correlation is weak
# -> Correlation is very statistically significant
"""
)
st.image('corr.png')

st.write(
    'We also created a database of variables that show significant ' \
    + 'patterns, and also recorded them in a dictionary. We used the ' \
    + 'analysis_list method, which creates a list of calculated variables ' \
    + '(r, R, p-value).'
)
st.code(
"""
insights = {}
for column in stateData.columns.tolist():
    if column != 'suicide_rate':
        if analysis_list(column, True)!= None:
            insights[column] = analysis_list(column)
            full[column] = analysis_list(column)
        else:
            full[column] = analysis_list(column)

for key, value in insights.items():
    print('{}: {}'.format(key, value))

# -> population: [-0.46141030848020154, 0.21289947277179475, \
0.0007445996809021158, 'weak', 'very statistically significant']
# -> white_population_rate: [0.3446746453536321, 0.11880061114965208, \
0.01423802591332206, 'weak', 'statistically significant']
# -> black_population_rate: [-0.4532914061795735, 0.20547309891625506, \
0.0009471105691989311, 'weak', 'very statistically significant']
# -> nominal_gdp: [-0.4723592741701852, 0.2231232838945842, \
0.0005332018687034512, 'weak', 'very statistically significant']
# -> nominal_gdp_per_capita: [-0.3856172846488639, 0.14870069021996293, \
0.005681643114344191, 'weak', 'very statistically significant']
# -> real_gdp: [-0.4574525725511598, 0.2092628561336741, \
0.0008378642671859441, 'weak', 'very statistically significant']
# -> non-christian_rate: [-0.45205031709283383, 0.2043494891837316, \
0.0009820794557001537, 'weak', 'very statistically significant']
# -> conservative_rate: [0.43585898266164574, 0.1899730527668448, \
0.0015568651062153223, 'weak', 'very statistically significant']
# -> liberal_rate: [-0.3814731983990535, 0.14552180109680365, \
0.0062683393671098386, 'weak', 'very statistically significant']
# -> urban_rate: [-0.4749903509585802, 0.22561583350375522, \
0.0004912642974694003, 'weak', 'very statistically significant']
# -> rural_rate: [0.4749903509585802, 0.22561583350375522, \
0.0004912642974694003, 'weak', 'very statistically significant']
# -> area: [0.4451681028847193, 0.19817463982598005, \
0.0011978399674817876, 'weak', 'very statistically significant']
# -> population_density: [-0.7151754326348221, 0.511475899444405, \
5.369841334596283e-09, 'strong', 'very statistically significant']
# -> unemployment_rate: [-0.42258118308335924, 0.17857485629613157, \
0.0022346464993665224, 'weak', 'very statistically significant']
"""
)

st.header("Heatmap")
st.image('geodata.png')

st.header('Conclusion')

st.write(
    'The religiosity of a state has nothing to do with its suicide ' \
    + 'rate. Sun levels associated with less depression, for some ' \
    + 'reason, do not affect suicide rates in the state. Perhaps this ' \
    + 'is due to the fact that the US climate is not sufficiently ' \
    + 'variable. This needs further clarification. High unemployment ' \
    + 'doesn\'t lead to high suicide rates. For some unknown reason, ' \
    + 'on the contrary, high unemployment in the state is associated ' \
    + 'with low suicide rates. The hypothesis of a single value of ' \
    + 'life (the connection between suicides and murders) ' \
    + 'was not confirmed.'
)

st.write(
    'Economic and scientific progress (or rather what we associate with ' \
    + 'these concepts: GDP, urbanization, political progressivism, religious ' \
    + 'tolerance) brings a decrease in the level of suicide. The hypothesis ' \
    + 'requires further reflection.'
)

st.write(
    'Note that the project already contains a set of ready-made analysis ' \
    + 'tools (analyze_this, analysis_list, plot_correlation), so in fact, ' \
    + 'in addition to new data, it requires only minor technical refinement.'
)

