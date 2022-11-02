/* First request:
We are trying to get the sumproduct of the price an the quantity, since we're looking to get the whole income per day.
So we need to GROUP BY the transactions per date then apply the sumproduct*/

SELECT date, SUM(prod_price * prod_qty) AS ventes 
            FROM transactions 
            where (date >= '01/01/2020' and  date <= '31/12/2020') 
            GROUP BY date;


/* Second request:

*/
