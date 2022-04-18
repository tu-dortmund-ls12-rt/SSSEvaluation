TP = 3
TN = 103
FP = 7
FN = 12

sensitivity  = TP / (TP+FN)
specificity  = TN / (TN+FP)
precision = TP/ (TP+FP)
slack_rate = FN / (TP+FN)
accuracy = (TP+TN) / (TP+TN+FP+FN)
Pseudo_defect_rate = FP / (TP+FP)
False_Omission_Rate = FN / (FN + TN)
Negative_Predictive_Value = TN / (FN + TN)
False_Positive_Rate =  FP / (FP + TN)

# 1.sensitivity 2.specificity 3.precision 4.slack_rate 5.accuracy 6.Pseudo defect rate
# 7.False Omission Rate 8.Negative_Predictive_Value 9.False_Positive_Rate

print('Sensitivity = ',sensitivity)
print('Specificity = ',specificity)
print('Precision = ',precision)
print('Slack_rate = ',slack_rate)
print('Accuracy = ',accuracy)
print('Pseudo_defect_rate = ',Pseudo_defect_rate)
print('False_Omission_Rate = ',False_Omission_Rate)
print('Negative_Predictive_Value = ',Negative_Predictive_Value)
print('False_Positive_Rate = ',False_Positive_Rate)