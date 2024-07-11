






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
