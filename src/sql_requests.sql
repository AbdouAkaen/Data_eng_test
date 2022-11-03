/* First request:
We are trying to get the sumproduct of the price an the quantity, since we're looking to get the whole income per day.
So we need to GROUP BY the transactions per date then apply the sumproduct*/

SELECT date, SUM(prod_price * prod_qty) AS ventes 
            FROM transactions 
            where (date >= '01/01/2020' and  date <= '31/12/2020') 
            GROUP BY date;


/* Second request:

*/

 SELECT transactions.client_id, SUM(CASE 
                                        WHEN product.product_type = 'MEUBLE' AND (date >= '01-01-2019' and date <= '31-12-2019') THEN 
                                        transactions.prod_price * transactions.prod_qty 
                                        ELSE 0 
                                        END) AS ventes_meubles 
                               ,SUM(CASE 
                                        WHEN product.product_type = 'DECO' AND (date >= '01-01-2019' and date <= '31-12-2019') THEN 
                                        transactions.prod_price * transactions.prod_qty 
                                        ELSE 0 END) AS ventes_deco 
                                from transactions INNER JOIN product 
                                ON transactions.prod_id = product.product_id 
                                GROUP BY transactions.client_id;
