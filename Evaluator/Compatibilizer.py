
class MethodCompatibilizer:
    
    def __init__(self, method, dataframe, canditates_column, **kwargs):
        self.method = method
        self.dataframe = dataframe
        self.canditates_column = canditates_column
        self.metrics_specs = kwargs.get("metrics_specs")
        
    def get_metric_columns(self) -> list:
        dataframe_columns = self.dataframe.columns
        metric_columns = [column for column in dataframe_columns if column != self.canditates_column]
        return metric_columns
    
    def get_specific_mcdm_features(self) -> dict:
        return {
            "promethee_ii": ["mode", "preference_limiar", "indiference_limiar"],
            "promethee_iii": ["mode", "preference_limiar", "indiference_limiar"],
            "promethee_iv": ["mode", "preference_limiar", "indiference_limiar"],
        }.get(self.method)
    
    def get_mcdm_features(self) -> list:
        standard_mcm_features = ["cost_criteria", "weight"]
        return standard_mcm_features + self.get_specific_mcdm_features()
    
    def check_metrics_specs(self):
        if isinstance(self.metrics_specs, type(None)):
            expected_dicionary = "{'metric_1': \"{'cost_criteria': 0, 'weight': 0.3}\"}"
            raise AttributeError(f"Expected a dictionary with metrics specifications like: {expected_dicionary}")
        for metric in self.get_metric_columns():
            for feature in self.get_mcdm_features():
                feature_value = self.metrics_specs.get(metric).get(feature, None)
                if isinstance(feature_value, type(None)):
                    raise AttributeError(f"Expected a {feature} feature on dictionay with metric specifications for metric {metric}")
        print('Compatibilizer Log: All metrics and specs OK!')


