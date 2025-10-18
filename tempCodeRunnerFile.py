regression model to predict calorie intake
X_nutrition = nutrition_df[['Protein (g)', 'Carbs (g)', 'Fat (g)']]
y_nutrition = nutrition_df['Total Calories']
X_train, X_test, y_train, y_test = train_test_split(X_nutrition, y_nutrition, test_size=0.2, random_state=42)
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X_train, y_train)

y_pred = rf_regressor.predict(X_test)
mape = mean_absolute_percentage_error(y_test, y_pred)
accuracy = 100 - (mape * 100)