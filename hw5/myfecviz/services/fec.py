from werkzeug.local import LocalProxy
import ujson

from myfecviz import get_db

db = LocalProxy(get_db)


def get_number_of_candidates():
    """Return the number of candidates registered with the FEC.

    This serves as just an example query.

    :returns: integer
    """
    # Execute database query
    db.execute("SELECT COUNT(*) FROM candidates;")
    results = db.fetchall()

    # Package into output
    return int(results[0][0])


def get_all_transaction_amounts():
    """Return all transaction amounts with the state that the contribution came from.

    For all committee contributions with a transaction_amt greater than zero,
    return every transaction amount with the state that the contribution came form.

    :return: List of dictionaries with 'state' and 'amount' keys
    """
    
    # Execute database query
    db.execute("SELECT state, transaction_amt FROM committee_contributions WHERE transaction_amt > 0")
    results = db.fetchall()
    final_results = list()

    for result in results:
        final_dict = {}
        final_dict['state'] = result[0]
        final_dict['amount'] = float(result[1])
        final_results.append(final_dict)
    # Package into output
    return final_results


def get_total_transaction_amounts_by_state():
    """Return a list of dicts containing the state and total contributions.

    For all committee contributions with a transaction_amt greater than zero,
    return a dictionary containing the state and total amount.

    :returns: List of dictionaries with 'state' and 'total_amount' keys
    """
    
    # Execute database query
    db.execute("SELECT state, SUM(transaction_amt) FROM committee_contributions WHERE transaction_amt > 0 GROUP BY state")
    results = db.fetchall()
    final_results = list()

    for result in results:
        final_dict = {}
        final_dict['state'] = result[0]
        final_dict['total_amount'] = float(result[1])
        final_results.append(final_dict)
    # Package into output
    return final_results
