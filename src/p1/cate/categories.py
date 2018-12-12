jobs = {'\"admin.\"': '0', '\"blue-collar\"': '1', '\"entrepreneur\"': '2', '\"housemaid\"': '3'
    , '\"management\"': '4', '\"retired\"': '5', '\"self-employed\"': '6', '\"services\"': '7', '\"student\"': '8'
    , '\"technician\"': '9', '\"unemployed\"': '10', '\"unknown\"': '11'}

maritals = {'\"divorced\"': '0','\"married\"': '1','\"single\"': '2','\"unknown\"': '3'}

educations = {'\"basic.4y\"': '0','\"basic.6y\"': '1','\"basic.9y\"': '2','\"high.school\"': '3',
              '\"illiterate\"': '4','\"professional.course\"': '5','\"university.degree\"': '6','\"unknown\"': '7'}

# no yes unknown
nyu = {'\"no\"': '0','\"yes\"': '1','\"unknown\"': '2'}

contacts = {'\"cellular\"': '0','\"telephone\"': '1'}

months = {'\"jan\"': '1', '\"feb\"': '2', '\"mar\"': '3', '\"apr\"': '4', '\"may\"': '5', '\"jun\"': '6',
          '\"jul\"': '7', '\"aug\"': '8', '\"sep\"': '9', '\"oct\"': '10', '\"nov\"': '11', '\"dec\"': '12'}

weekday = {'\"mon\"': '1','\"tue\"': '2','\"wed\"': '3','\"thu\"': '4','\"fri\"': '5'}

poutcomes = {'\"failure\"': '0','\"nonexistent\"': '1','\"success\"': '2'}

# is the ith attribute categorical, false means numeric
is_cat = [False, True, True, True, True, True, True, True, True, True,
          False, False, False, True, False, False, False, False, False]

true_label = '1'
false_label = '0'

labels = {'"yes"': true_label, '"no"': false_label}
