SELECT u.name, u.email, SUM(p.price * o.quantity) AS total_spent
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN products p ON o.product_id = p.id
WHERE p.category = 'Electronics'
GROUP BY u.id, u.name, u.email
HAVING COUNT(o.id) >= 3 AND SUM(p.price * o.quantity) > 1000
ORDER BY total_spent DESC;