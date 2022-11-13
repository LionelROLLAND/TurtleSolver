import typing

CODES = {
            'OPTIMAL':1,
            'UNBD':2,
            'INFEAS':3,
            'INF_OR_UNBD':4,
            'OPT_INFEAS':5,
            'NOT_OPTI':6,
            'TIME_LIM':11,
            'DET_TIME_LIM':25,
            'MIP_OPTIMAL':101,
            'MIP_TOL_OPTIMAL':102,
            'MIP_INFEAS':103,
            'MIP_SOL_LIM':104, # ?
            'MIP_NODE_LIM_FEAS':105, # ? A solution exists, but node limit reached
            'MIP_NODE_LIMIT_INFEAS':106,
            'MIP_TIME_LIM_FEAS':107,
            'MIP_TIME_LIM_INFEAS':108,
            'MIP_FAIL_FEAS':109,
            'MIP_FAIL_INFEAS':110,
            'MIP_MEM_LIM_FEAS':111,
            'MIP_MEM_LIM_INFEAS':112,
            'MIP_ABORT_FEAS':113,
            'MIP_ABORT_INFEAS':114,
            'MIP_FAIL_FEAS_NO_TREE':116,
            'MIP_FAIL_INFEAS_NO_TREE':117,
            'MIP_UNBD':118,
            'MIP_INF_OR_UNBD':119,
            'MIP_POPULATESOL_LIM':128,
            'MIP_OPTIMAL_POPULATED':129,
            'MIP_TOL_OPTIMAL_POPULATED':130,
            'MIP_DET_TIME_LIM_FEAS':131,
            'MIP_DET_TIME_LIM_INFEAS':132,
        }


def error_str(error:int) -> str:
    if error == CODES['NOT_OPTI']:
        return "Numerical difficulties, the solution may not be optimal."
    if error == CODES['INF_OR_UNBD'] or error == CODES['MIP_INF_OR_UNBD']:
        return "Problem infeasible or unbounded."
    if error == CODES['INFEAS'] or error == CODES['MIP_INFEAS']:
        return "Problem infeasible."
    if error == CODES['DET_TIME_LIM'] or error == CODES['TIME_LIM']:
        return "Time limit for the resoltion exceeded, problem not solved."
    if error == CODES['OPT_INFEAS']:
        return (
            "I don't understand this error, "
            "the associated solution status code is 5 "
            "(CPX_STAT_OPTIMAL_INFEAS), go check the doc "
            "of CPLEX if you want details."
               )
    if error == CODES['UNBD'] or error == CODES['MIP_UNBD']:
        return "Problem unbounded."
    if error == CODES['MIP_SOL_LIM']:
        return (
            "I don't understand this error, "
            "the associated solution status code is 104 "
            "(CPXMIP_SOL_LIM, \"The limit on mixed integer "
            "solutions has been reached\"), go check the doc "
            "of CPLEX if you want details."
               )
    if error == CODES['MIP_NODE_LIM_FEAS']:
        return (
            "I don't understand this error, "
            "the associated solution status code is 105 "
            "(CPXMIP_NODE_LIM_FEAS, a solution exists but "
            "\"node limit has been exceeded\"), go check the doc "
            "of CPLEX if you want details."
               )
    if error == CODES['MIP_NODE_LIM_INFEAS']:
        return (
            "I don't understand this error, "
            "the associated solution status code is 106 "
            "(CPXMIP_NODE_LIM_INFEAS, the problem is infeasible and "
            "\"node limit has been exceeded\"), go check the doc "
            "of CPLEX if you want details."
               )
    if error == CODES['MIP_TIME_LIM_FEAS'] or error == CODES['MIP_DET_TIME_LIM_FEAS']:
        return "A solution exists but the time limit has been reached."
    if error == CODES['MIP_TIME_LIM_INFEAS'] or error == CODES['MIP_DET_TIME_LIM_INFEAS']:
        return "The problem is infeasible and the time limit has been reached."
    if error == CODES['MIP_FAIL_FEAS']:
        return "A solution exists but CPLEX encountered an error."
    if error == CODES['MIP_FAIL_INFEAS']:
        return "The problem is infeasible and CPLEX encountered an error."
    if error == CODES['MIP_MEM_LIM_FEAS']:
        return "A solution exists but the memory limit has been reached."
    if error == CODES['MIP_MEM_LIM_INFEAS']:
        return "The problem is infeasible and the memory limit has been reached."
    if error == CODES['MIP_ABORT_FEAS']:
        return "A solution exists but CPLEX was interrupted early."
    if error == CODES['MIP_ABORT_INFEAS']:
        return "The problem is infeasible and CPLEX was interrupted early."
    if error == CODES['MIP_FAIL_FEAS_NO_TREE']:
        return (
            "I don't understand this error, "
            "the associated solution status code is 116 "
            "(CPXMIP_FAIL_FEAS_NO_TREE, a solution exists but "
            "\"out of memory, no tree available\"), go check the doc "
            "of CPLEX if you want details."
               )
    if error == CODES['MIP_FAIL_INFEAS_NO_TREE']:
        return (
            "I don't understand this error, "
            "the associated solution status code is 117 "
            "(CPXMIP_FAIL_INFEAS_NO_TREE, the problem is infeasible and "
            "\"out of memory, no tree available\"), go check the doc "
            "of CPLEX if you want details."
               )
    return "Unknown error status code = " + str(error)