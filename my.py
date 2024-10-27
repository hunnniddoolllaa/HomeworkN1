import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

train_df = pd.read_csv('train.csv')
questions_df = pd.read_csv('questions.csv')
lectures_df = pd.read_csv('lectures.csv')

print(train_df.head())
print(questions_df.head())
print(lectures_df.head())
print(train_df.info())

# Общая информация о типе данных
print(train_df.info())

#процент верных ответов
train_df['prior_correctness'] = train_df.groupby('user_id')['answered_correctly'].transform('mean')

#количество занятий и лекций в целом,  количество контента
user_content_count = train_df.groupby('user_id').size().reset_index(name='content_count')


#процент   и количество неверных ответов
answered_not_correctness = train_df[train_df['answered_correctly'] == 0]

user_incorrect_counts = answered_not_correctness.groupby('user_id').size().reset_index(name='incorrect_count')

# Построим график
fig = px.bar(user_incorrect_counts, x= 'user_id',y='incorrect_count',title='Количество неправильных ответов по пользователям' )
fig.update_layout(xaxis_title='user_id',yaxis_title='Количесвто неправильных ответов')
fig.show()

#количество пропущенных занятий
missed_classes = train_df.isnull().sum()


#количество и процент занятий и лекций отдельно
content_type_count = train_df.groupby(['user_id','content_type_id']).size().unstack(fill_value=0)
content_type_count.columns = ['questions_count', 'lecture_count']
content_type_count['lecture_question_ratio'] = content_type_count['lecture_count'] / (content_type_count['questions_count'] + 1)
#print(content_type_count.head())

# Построим график
fig = px.bar(content_type_count.reset_index(),x='user_id',y='lecture_question_ratio',title='Соотношение лекций к вопросам для каждого пользователя')
fig.update_layout(xaxis_title='user_id',yaxis_title = 'Соотношение лекций к вопросам')
fig.show()

# среднее время затраченное на ответ
train_df['time_diff'] = train_df.groupby('user_id')['timestamp'].diff()
user_avg_time = train_df.groupby('user_id')['time_diff'].mean()
#print(user_avg_time.head())

# Построим график
fig = px.bar(user_avg_time.reset_index(),x='user_id',y='time_diff',title='Среднее время между действиями для каждого пользователя')
fig.update_layout(xaxis_title='user_id', yaxis_title='Среднее время между действиями (мс)')
fig.show()

#Среднее значение верных ответов по контейнеру/ средняя точность ответов
container_accuracy = train_df.groupby('task_container_id')['answered_correctly'].mean()
container_accuracy.columns = ['task_container_id', 'answered_correctly']


#Средняя скорость пользователя при ответе на вопрос
train_df['prior_question_elapsed_time'].fillna(0, inplace= True)
user_prior_time = train_df.groupby('user_id')['prior_question_elapsed_time'].mean().reset_index()
user_prior_time.columns = ['user_id', 'avg_prior_question_time']

# Процент полученных объяснений и показанных верных ответов

explanation_rate = train_df.groupby('user_id')['prior_question_had_explanation'].mean().reset_index()
explanation_rate.columns = ['user_id', 'explanation_rate']


# Находим процентное соотношение правильных ответов для каждого пользователя
train_df = train_df.merge(questions_df[['question_id','correct_answer']],left_on='content_id',right_on='question_id',how='left')
train_df['is_correct'] = (train_df['user_answer'] == train_df['correct_answer']).astype(int)
correct_answer_rate = train_df.groupby('user_id')['is_correct'].mean().reset_index()
correct_answer_rate.columns = ['user_id','correct_answer_rate']

# Построим график
fig = px.histogram(correct_answer_rate, x= 'correct_answer_rate', nbins= 50, title='Распределение процентов правильных ответов' )
fig.update_layout(xaxis_title = 'Средний  процент правильных ответов', yaxsis_title ='Количество пользователей')
fig.show()