import json
import numpy as np
import matplotlib.pyplot as plt

# Open the JSON file
with open('Testing-relationship-closeness-through-food-sharing_all-responses-identifiable.json', 'r') as file:
    # Load JSON data from the file
    data = json.load(file)

# 12 total
trials = [
    '12-null',
    '14-null',
    '16-null',
    '18-null',
    '20-null',
    '22-null',
    '24-null',
    '26-null',
    '28-null',
    '30-null',
    '32-null',
    '34-null'
]

fam_answers = [
    'option1', # juice with one straw
    'option1', # lollipop
    'option2', # applesauce with one spoon
    'option1', # ice cream cone
    'option1', # scooter # PROBLEM SLIDE (check audio --> requires watching through videos)
    'option1', # jump rope
    'option1', # sand toys
    'option1', # legos
    'option1', # candies
    'option1', # cookies
    'option1', # grapes
    'option1' # crackers
]

non_fam_answers = [
    'option2', 
    'option2',
    'option1',
    'option2',
    'option2',
    'option2',
    'option2',
    'option2',
    'option2', 
    'option2',
    'option2', 
    'option2'
]

# grouping arrays
condition_groupings = [ 
    [0, 1, 2, 3],
    [8, 9, 10, 11],
    [4, 5],
    [6, 7]
]

# saliva_sharing = [0, 1, 2, 3]

# divisible_food = [8, 9, 10, 11]

# toy_sharing = [4, 5]

# divisible_toys = [6, 7]

# timing details - frameDuration
times_per_trial = [
    [],[],[],[],[],[],[],[],[],[],[],[]
]

# results
fam_per_trial_count = np.zeros(12, dtype=int)
non_fam_per_trial_count = np.zeros(12, dtype=int)
idk_per_trial_count = np.zeros(12, dtype=int)

total_response_count = 0
for resp in data:
    if not resp["response"]["completed"]:
        continue
    elif resp["response"]["eligibility"] != ["Eligible"]:
        continue
    else:
        total_response_count += 1
        # print(resp['child']['hashed_id'])

        for trial_idx, frame_name in enumerate(trials):
            if "selectedImage" in resp["exp_data"][frame_name]:
                selection = resp["exp_data"][frame_name]["selectedImage"]
                if selection == fam_answers[trial_idx]:
                    fam_per_trial_count[trial_idx] += 1
                elif selection == non_fam_answers[trial_idx]:
                    non_fam_per_trial_count[trial_idx] += 1
                elif selection == "option3":
                    idk_per_trial_count[trial_idx] += 1
                times_per_trial[trial_idx].append(resp["exp_data"][frame_name]["frameDuration"])

total_excluding_idk = fam_per_trial_count + non_fam_per_trial_count
percentage_chose_fam = fam_per_trial_count / total_excluding_idk
max_time = max([max(times) for times in times_per_trial])
normalized_times_per_trial = [[time / max_time for time in times] for times in times_per_trial]
print('MAXTIME: ',max_time, normalized_times_per_trial)
print("TIMES: ", times_per_trial)

print("Total number of responses: ", total_response_count)
print("FAMILY: ", fam_per_trial_count)
print("NON-FAMILY: ", non_fam_per_trial_count)
print("I don't know: ", idk_per_trial_count)

print("Total (excluding NA responses): ", total_excluding_idk)

print("Percentage that chose family: ", percentage_chose_fam)

# graph 1
x_labels_1 = [
    'juice',
    'lollipop',
    'applesauce',
    'ice cream cone',
    'candies',
    'cookies',
    'grapes',
    'crackers',
    'scooter',
    'jump rope',
    'sand toys',
    'legos'
]
x_axis_1 = np.arange(12)
# changing order of data to match second graph
percentage_chose_fam = np.concatenate((percentage_chose_fam[:4], percentage_chose_fam[-4:], percentage_chose_fam[4:6], percentage_chose_fam[6:8]))

plt.figure(figsize=(16, 8))
colors_1 = ['tomato', 'tomato', 'tomato', 'tomato', 'cornflowerblue', 'cornflowerblue', 'cornflowerblue', 'cornflowerblue', 'cornflowerblue', 'cornflowerblue', 'cornflowerblue', 'cornflowerblue']
plt.bar(x_axis_1, percentage_chose_fam, color=colors_1) #, 'ro')
plt.xticks(x_axis_1, x_labels_1)
plt.xlabel("Condition")
plt.ylabel("Percentage that chose family")
plt.title("Percentage of children that chose family over friend per condition")
plt.ylim(0.0, 1.0)
# for i, times in enumerate(normalized_times_per_trial):
#     times_x = [np.random.uniform(i-0.25, i+0.25) for n in range(len(times))]
#     plt.plot(times_x, times, 'o', color='palegoldenrod', label='time taken to answer (max=81s)')
plt.savefig("result_plots/per_trial.png")

# averaged percentages by groups
grouped_percentages = [] # should be length of 4
for group in condition_groupings:
    sum_ = 0
    num_in_group = len(group)
    for idx in group:
        sum_ += percentage_chose_fam[idx]
    avg = sum_ / num_in_group
    grouped_percentages.append(avg)

# graph 2
x_labels_2 = [
    'saliva-sharing food',
    'food that can be divided',
    'toys that cannot be divided',
    'toys that can be divided'
]
x_axis_2 = np.arange(4)

plt.figure(figsize=(14, 12))
colors_2 = ['tomato', 'cornflowerblue', 'cornflowerblue', 'cornflowerblue']
plt.bar(x_axis_2, grouped_percentages, color=colors_2)
plt.xticks(x_axis_2, x_labels_2)
plt.xlabel("Type of condition")
plt.ylabel("Percentage that chose family")
plt.title("Percentage of children that chose family over friend per type of condition")
plt.ylim(0.0, 1.0)
plt.savefig("result_plots/per_grouping.png")
