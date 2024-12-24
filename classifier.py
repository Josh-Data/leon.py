{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "113aeab6-02d8-4448-b4d0-884d4172a7bf",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import xgboost as xgb\n",
    "import numpy as np\n",
    "from sklearn.model_selection import train_test_split as tts\n",
    "\n",
    "# Load the dataset\n",
    "df = pd.read_csv(\"/Users/joshsingh/Downloads/data.csv\")\n",
    "\n",
    "# Prepare the training and testing data\n",
    "length = df.shape[0]\n",
    "main = int(length * 0.8)\n",
    "trainer = df.iloc[:main]\n",
    "tester = df.iloc[main:]\n",
    "X = trainer.drop(columns=[\"fail\"])\n",
    "y = trainer.fail\n",
    "X_train, X_val, y_train, y_val = tts(X, y, train_size=0.8, random_state=42)\n",
    "\n",
    "# Train the model\n",
    "model = xgb.XGBClassifier(n_estimators=20)\n",
    "model.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_val, y_val)])\n",
    "\n",
    "# Streamlit interface\n",
    "st.title('Prediction Model Interface')\n",
    "\n",
    "# Get the feature columns for input\n",
    "feature_columns = X.columns\n",
    "\n",
    "# Input fields for each feature\n",
    "feature_inputs = {}\n",
    "for feature in feature_columns:\n",
    "    feature_inputs[feature] = st.number_input(f'Enter value for {feature}', min_value=float(df[feature].min()), max_value=float(df[feature].max()))\n",
    "\n",
    "# When the \"Predict\" button is clicked\n",
    "if st.button('Predict'):\n",
    "    # Prepare the input data in the correct format\n",
    "    input_data = np.array([list(feature_inputs.values())])\n",
    "    \n",
    "    # Predict using the trained model\n",
    "    result = model.predict(input_data)\n",
    "    \n",
    "    # Show the prediction result\n",
    "    st.write(f'Prediction: {result[0]}')  # Display the predicted class (0 or 1)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
