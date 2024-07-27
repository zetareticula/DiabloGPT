#include <vector>
#include <algorithm>

// Add any other necessary header files here

// Add any necessary namespaces here

// Define your function or class here

// Rest of your code

void identity_leave(const std::vector<bool>& relevantScope, const std::vector<bool>& featureScope, const std::vector<bool>& inverse, std::vector<std::vector<floating_data_type>>& nodeIntermediateResult, const std::vector<floating_data_type>& mean, const std::vector<floating_data_type>& inverted_mean, const std::vector<std::vector<floating_data_type>>& unique_values, const std::vector<std::vector<floating_data_type>>& prob_sum, const std::vector<bool>& leftMinusInf, const std::vector<floating_data_type>& leftCondition, const std::vector<bool>& rightMinusInf, const std::vector<floating_data_type>& rightCondition, const std::vector<floating_data_type>& nullValue, const std::vector<bool>& leftIncluded, const std::vector<bool>& rightIncluded, const std::vector<floating_data_type>& null_value_prob, const std::vector<int>& node_id, const std::vector<std::string>& final_assert) {
    for (int i = 0; i < node_id.size(); i++) {
        if (relevantScope[node_id[i]]) {
            if (featureScope[node_id[i]]) {
                if (inverse[node_id[i]]) {
                    nodeIntermediateResult[node_id[i]] = inverted_mean[i];
                } else {
                    nodeIntermediateResult[node_id[i]] = mean[i];
                }
            } else {
                std::vector<floating_data_type> uniqueVals = unique_values[i];
                std::vector<floating_data_type> probSum = prob_sum[i];
                int leftIdx = 0;
                if (!leftMinusInf[node_id[i]]) {
                    auto leftBoundIdx = std::lower_bound(uniqueVals.begin(), uniqueVals.end(), leftCondition[node_id[i]]);
                    leftIdx = leftBoundIdx - uniqueVals.begin();
                }
                int rightIdx = uniqueVals.size();
                if (!rightMinusInf[node_id[i]]) {
                    auto rightBoundIdx = std::upper_bound(uniqueVals.begin(), uniqueVals.end(), rightCondition[node_id[i]]);
                    rightIdx = rightBoundIdx - uniqueVals.begin();
                }
                nodeIntermediateResult[node_id[i]] = probSum[rightIdx] - probSum[leftIdx];
                if (((leftMinusInf[node_id[i]] || leftCondition[node_id[i]] < nullValue[node_id[i]]) && (rightMinusInf[node_id[i]] || rightCondition[node_id[i]] > nullValue[node_id[i]])) ||
                    (!leftMinusInf[node_id[i]] && (nullValue[node_id[i]] == leftCondition[node_id[i]]) && leftIncluded[node_id[i]]) ||
                    (!rightMinusInf[node_id[i]] && (nullValue[node_id[i]] == rightCondition[node_id[i]]) && rightIncluded[node_id[i]])) {
                    nodeIntermediateResult[node_id[i]] -= null_value_prob[i];
                }
                if (!leftIncluded[node_id[i]] && !leftMinusInf[node_id[i]] && leftCondition[node_id[i]] == uniqueVals[leftIdx]) {
                    nodeIntermediateResult[node_id[i]] -= probSum[leftIdx + 1] - probSum[leftIdx];
                }
                if (!rightIncluded[node_id[i]] && !rightMinusInf[node_id[i]] && rightCondition[node_id[i]] == uniqueVals[rightIdx] && leftCondition[node_id[i]] != rightCondition[node_id[i]]) {
                    nodeIntermediateResult[node_id[i]] -= probSum[rightIdx] - probSum[rightIdx - 1];
                }
            }
            // $final_assert
        }
    }
}
if (relevantScope[{node_scope}]) {{
    if (featureScope[{node_scope}]) {{
        if (inverse{node_scope}) {{
            nodeIntermediateResult[{node_id}] = {inverted_mean};
        }} else {{
            nodeIntermediateResult[{node_id}] = {mean};
        }}
    }} else {{

        vector<{floating_data_type}> uniqueVals{node_id}{{ {unique_values} }};
        vector<{floating_data_type}> probSum{node_id}{{ {prob_sum} }};

        // search right and left bounds via binary search
        int leftIdx{node_id} = 0;
        if (!leftMinusInf{node_scope}) {{
            vector<{floating_data_type}>::iterator leftBoundIdx{node_id};
            leftBoundIdx{node_id} = std::lower_bound(uniqueVals{node_id}.begin(), uniqueVals{node_id}.end(), leftCondition{node_scope});
            leftIdx{node_id} = leftBoundIdx{node_id} - uniqueVals{node_id}.begin();
        }}

        int rightIdx{node_id} = uniqueVals{node_id}.size();
        if (!rightMinusInf{node_scope}) {{
            vector<{floating_data_type}>::iterator rightBoundIdx{node_id};
            rightBoundIdx{node_id} = std::upper_bound(uniqueVals{node_id}.begin(), uniqueVals{node_id}.end(), rightCondition{node_scope});
            rightIdx{node_id} = rightBoundIdx{node_id} - uniqueVals{node_id}.begin();
        }}

        nodeIntermediateResult[{node_id}] = probSum{node_id}[rightIdx{node_id}] - probSum{node_id}[leftIdx{node_id}];

        // exclude null value if it was included before
        if (((leftMinusInf{node_scope} || leftCondition{node_scope} < nullValue{node_scope}) && (rightMinusInf{node_scope} || rightCondition{node_scope} > nullValue{node_scope})) ||
            (!leftMinusInf{node_scope} && (nullValue{node_scope} == leftCondition{node_scope}) && leftIncluded{node_scope}) ||
            (!rightMinusInf{node_scope} && (nullValue{node_scope} == rightCondition{node_scope}) && rightIncluded{node_scope})) {{
            nodeIntermediateResult[{node_id}] -= {null_value_prob}; // null value prob
        }}

        // left value should not be included in interval
        if (!leftIncluded{node_scope} && !leftMinusInf{node_scope} && leftCondition{node_scope} == uniqueVals{node_id}[leftIdx{node_id}]) {{
            nodeIntermediateResult[{node_id}] -= probSum{node_id}[leftIdx{node_id} + 1] - probSum{node_id}[leftIdx{node_id}];
        }}

        //same for right
        if (!rightIncluded{node_scope} && !rightMinusInf{node_scope} && rightCondition{node_scope} == uniqueVals{node_id}[rightIdx{node_id}-{node_id}] && leftCondition{node_scope} != rightCondition{node_scope}) {{
            nodeIntermediateResult[{node_id}] -= probSum{node_id}[rightIdx{node_id}] - probSum{node_id}[rightIdx{node_id} - 1];
        }}
    }}
    {final_assert}
}}
void CategoricalLeave{node_id}::apply(const std::vector<std::vector<floating_data_type>>& nodeIntermediateResult, std::vector<floating_data_type>& nodeResult) const {{
    nodeResult[{node_id}] = nodeIntermediateResult[{node_id}];
}}
// End of comparison
