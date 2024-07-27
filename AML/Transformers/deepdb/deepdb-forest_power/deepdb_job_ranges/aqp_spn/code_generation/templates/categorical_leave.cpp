
#include <vector>

class CategoricalLeave {
public:
    CategoricalLeave(int node_id, int node_scope, int nullValueIdx, const std::vector<int>& possibleValues, bool relevantScope, floating_data_type node_p, const std::string& final_assert)
        : node_id(node_id), node_scope(node_scope), nullValueIdx(nullValueIdx), possibleValues(possibleValues), relevantScope(relevantScope), node_p(node_p), final_assert(final_assert) {}

    void calculate(std::vector<floating_data_type>& nodeIntermediateResult) const {
        if (relevantScope) {
            floating_data_type probsNode{node_id}[] = {node_p};
            // Check for null value
            if (nullValueIdx != -1) {
                nodeIntermediateResult[node_id] = 1 - probsNode[node_id][nullValueIdx];
            } else {
                for (int idx : possibleValues) {
                    nodeIntermediateResult[node_id] += probsNode[node_id][idx];
                }
            }
        }
        {final_assert}
    }

    void apply(const std::vector<std::vector<floating_data_type>>& nodeIntermediateResult, std::vector<floating_data_type>& nodeResult) const {
        nodeResult[node_id] = nodeIntermediateResult[node_id];
    }

private:
    int node_id;
    int node_scope;
    int nullValueIdx;
    std::vector<int> possibleValues;
    bool relevantScope;
    floating_data_type node_p;
    std::string final_assert;
};





    if (relevantScope[{node_scope}]) {
    
        floating_data_type} probsNode{node_id}[] = { {node_p} };

    // Check for null value
    if (nullValueIdx{node_scope} != -1) {
        nodeIntermediateResult[{node_id}] = 1 - probsNode{node_id}[nullValueIdx{node_scope}];
    } else {
        for (int idx : possibleValues{node_scope}) {
            nodeIntermediateResult[{node_id}] += probsNode{node_id}[idx];
        }
    }
    {final_assert}
}

void CategoricalLeave{node_id}::apply(const std::vector<std::vector<floating_data_type>>& nodeIntermediateResult, std::vector<floating_data_type>& nodeResult) const {
    nodeResult[{node_id}] = nodeIntermediateResult[{node_id}];
}
