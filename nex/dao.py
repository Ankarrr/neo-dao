from boa.interop.Neo.Runtime import CheckWitness, Notify
from boa.interop.Neo.Action import RegisterAction
from boa.interop.Neo.Storage import *
from boa.builtins import concat

from boa_test.example.demo.nex.token import *

PROPOSAL_LIST_KEY = 'proposalList'
TOTAL_PROPOSAL_AMOUNT = 'totalproposalAmount'   

def handle_dao(ctx, operation, args):

    # Add a new proposal 
    if operation == 'addProposal':
        if len(args) == 3:
            # args[0]: from address
            # args[1]: ipfs hash
            # args[2]: amount of NEO
            # args[3]: voting threshold
            return do_add_proposal(ctx, args[0], args[1], args[2], args[3])

    # Vote for a propasal
    elif operation == 'voteforProposal':
        if len(args) == 1:
            # args[0]: from address 
            # args[1]: proposal id
            return do_vote_for_proposal(ctx, args[0], args[1])

    # Claim the NEO if the proposal is approved
    elif openration == 'finalizeProposal':
        if len(args) == 0:
            return do_finalize_proposal()

    return False


def do_add_proposal(ctx, t_from, ipfs_hash, amount, threshold):

    if amount <= 0:
        return False

    if CheckWitness(t_from):

        from_val = Get(ctx, t_from)

        # Only the token holder can add new proposal
        if from_val == 0:
            print("insufficient funds")
            return False

        # Add totalProposal
        totalProposal = Get(ctx, TOTAL_PROPOSAL_AMOUNT)
        Put(ctx, TOTAL_PROPOSAL_AMOUNT, totalProposal + 1)
        proposal_id = totalProposal + 1

        # Deserialize proposal list
        serialized = Get(ctx, PROPOSAL_LIST_KEY)
        proposal_list = deserialize_bytearray(serialized)

        # Create new proposal
        initialVotes = 0
    
        # A proposal include:
        # 1. Id: string
        # 2. Ipfs_hash: string
        # 3. Neo amount: int
        # 4. Threshold: int
        # 5. Vote counter: int
        # 6. Approved: Boolean
        # 7. Proposer address: string
        new_proposal = [proposal_id, ipfs_hash, str(amount), str(threshold), str(initialVotes), "False", t_from]

        proposal_list.append(serialized_array(new_proposal))

        # Serialize again and put it
        to_save = serialize_array(proposal_list)
        Put(ctx, PROPOSAL_LIST_KEY, to_save)

        return True

    else:
        print("from address is not the tx sender")

    return False

def do_vote_for_proposal(ctx, t_from, proposal_id):

    if CheckWitness(t_from):

        from_val = Get(ctx, t_from)

        # Only the token holder can vote for a proposal
        if from_val == 0:
            print("insufficient funds")
            return False

        # Deserialize proposal list
        serialized = Get(ctx, PROPOSAL_LIST_KEY)
        proposal_list = deserialize_bytearray(serialized)

        # Find the proposal according to "proposal_id" and add the from_val to the proposal's current vote amount

        # Serialize again and put it
        to_save = serialize_array(proposal_list)
        Put(ctx, PROPOSAL_LIST_KEY, to_save)

        return True
    else:
        print("from address is not the tx sender")

    return False

def do_finalize_proposal(ctx, t_from):

    # If proposal[threshold] >= proposal[totalVotes]
    #   If proposal["Approved"] == True
    #       return False   
    #   else 
    #       1. Set "Approved" to True
    #       2. claim the NEO. Question: Can I transfer the NEO in the contract to another one?
    #       return True
    # else
    return False