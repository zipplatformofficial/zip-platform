// Store Products endpoint
const { query } = require('./db');

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle preflight
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  try {
    if (event.httpMethod === 'GET') {
      // Get all products
      const result = await query(
        `SELECT id, name, description, category, price, stock_quantity,
                image_url, vendor_id, is_active, created_at
         FROM store_products
         WHERE is_active = true AND stock_quantity > 0
         ORDER BY name`
      );

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(result.rows)
      };
    }

    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  } catch (error) {
    console.error('Store products error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        detail: 'Failed to fetch products',
        error: error.message
      })
    };
  }
};
