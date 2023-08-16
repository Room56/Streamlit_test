import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Загрузка и отображение датасета
def load_dataset():
    uploaded_file = st.file_uploader("Загрузить датасет (CSV)", type="csv")
    if uploaded_file is not None:
        try:
            dataset = pd.read_csv(uploaded_file)
            return dataset
        except Exception as e:
            st.error("Ошибка при загрузке датасета")
            st.error(e)
    else:
        st.warning("Пожалуйста, загрузите датасет в формате CSV")

# Проверка гипотезы
def perform_hypothesis_test(data, var1, var2, test):
    if test == "t-тест":
        result = stats.ttest_ind(data.dropna()[var1], data.dropna()[var2])
        st.write("t-статистика:", result.statistic)
        st.write("p-значение:", result.pvalue)
    elif test == "Chi-squared test":
        table = pd.crosstab(data.dropna()[var1], data.dropna()[var2])
        result = stats.chisquare(table)
        st.write("Статистика хи-квадрат:", result.statistic)
        st.write("p-значение:", result.pvalue)

# Основной код
def main():
    st.title("Исследование датасета")

    dataset = load_dataset()

    if dataset is not None:

        st.dataframe(dataset.head())
        dataset.dtypes

        variables = list(dataset.columns)

        var1 = st.selectbox("Выберите первую переменную:", variables)
        var2 = st.selectbox("Выберите вторую переменную:", variables)

        if var1 != var2:
            with st.expander("Визуализация"):
                # Визуализация первой переменной
                st.subheader("Распределение " + var1)
                if dataset[var1].dtype == "object":
                    fig, ax = plt.subplots()
                    ax.pie(dataset[var1].value_counts(), labels=dataset[var1].value_counts().index, autopct="%1.1f%%")
                    st.pyplot(fig)
                   # fig = plt.figure(figsize=(8, 6))
                   # sns.countplot(data=dataset, x=var1)
                   # plt.xticks(rotation=45)
                   # st.pyplot(fig)

                else:
                    fig = plt.figure(figsize=(8, 6))
                    sns.histplot(data=dataset, x=var1, kde=True)
                    st.pyplot(fig)

                # Визуализация второй переменной
                st.subheader("Распределение " + var2)
                if dataset[var2].dtype == "object":
                    fig, ax = plt.subplots()
                    ax.pie(dataset[var2].value_counts(), labels=dataset[var2].value_counts().index, autopct="%1.1f%%")
                    st.pyplot(fig)
                   # fig = plt.figure(figsize=(8, 6))
                   # sns.countplot(data=dataset, x=var2)
                   # plt.xticks(rotation=45)
                   # st.pyplot(fig)

                else:
                    fig = plt.figure(figsize=(8, 6))
                    sns.histplot(data=dataset, x=var2, kde=True)
                    st.pyplot(fig)

        test = st.selectbox(
            "Выберите проверочный алгоритм:", ["t-тест", "Chi-squared test"]
        )
        st.subheader("Результаты проверки гипотезы")
        if var1 != var2:
            perform_hypothesis_test(dataset, var1, var2, test)


if __name__ == "__main__":
    main()