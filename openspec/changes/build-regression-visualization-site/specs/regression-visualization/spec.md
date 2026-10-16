## ADDED Requirements

### Requirement: Dataset selection and exploration

The system SHALL allow a visitor to select either the 50 Startups or Boston Housing dataset and view a summary plus exploratory visualizations for the selected dataset.

#### Scenario: Visitor changes the dataset

- **WHEN** the visitor selects a supported dataset
- **THEN** the system displays its name, record count, columns, target field, summary information, and exploration charts

### Requirement: Regression experiment

The system SHALL run a test-set regression experiment for a supported dataset and model selection.

#### Scenario: Visitor runs a random forest experiment

- **WHEN** the visitor selects a dataset, the random forest model, and a valid training proportion then starts an experiment
- **THEN** the system returns MAE, RMSE, R², actual-versus-predicted values, residual values, and feature importance values

### Requirement: Model comparison support

The system SHALL support linear regression, decision tree regression, and random forest regression for both datasets.

#### Scenario: Visitor selects a supported model

- **WHEN** the visitor runs an experiment using any supported model
- **THEN** the system evaluates the selected model using the same reproducible test-split policy

### Requirement: Deployable web application

The system SHALL be deployable with the front end served over HTTPS and the model API reachable over HTTPS.

#### Scenario: Deployed site starts an experiment

- **WHEN** a visitor opens the deployed site and starts a valid experiment
- **THEN** the browser can retrieve and display the experiment result without mixed-content or cross-origin failure

### Requirement: Educational dataset disclosure

The system SHALL show the datasets' sources and disclose that Boston Housing is included for instructional demonstration only.

#### Scenario: Visitor opens the information section

- **WHEN** the visitor views the dataset information section
- **THEN** the system displays source attribution and the Boston Housing educational-use notice
