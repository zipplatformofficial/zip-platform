// Get all vehicles
const { query } = require('./db');

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    // Query parameters for filtering
    const params = event.queryStringParameters || {};
    const { make, transmission, min_price, max_price, seats, available } = params;

    let sql = `
      SELECT
        v.id, v.make, v.model, v.year, v.color,
        v.license_plate, v.transmission, v.fuel_type,
        v.seats, v.daily_rate as price_per_day, v.mileage,
        v.image_url as image, v.is_available, v.location,
        v.features, v.description, v.created_at
      FROM vehicles v
      WHERE 1=1
    `;
    const queryParams = [];
    let paramIndex = 1;

    // Apply filters
    if (make) {
      sql += ` AND LOWER(v.make) LIKE LOWER($${paramIndex})`;
      queryParams.push(`%${make}%`);
      paramIndex++;
    }

    if (transmission) {
      sql += ` AND LOWER(v.transmission) = LOWER($${paramIndex})`;
      queryParams.push(transmission);
      paramIndex++;
    }

    if (min_price) {
      sql += ` AND v.daily_rate >= $${paramIndex}`;
      queryParams.push(parseFloat(min_price));
      paramIndex++;
    }

    if (max_price) {
      sql += ` AND v.daily_rate <= $${paramIndex}`;
      queryParams.push(parseFloat(max_price));
      paramIndex++;
    }

    if (seats) {
      sql += ` AND v.seats >= $${paramIndex}`;
      queryParams.push(parseInt(seats));
      paramIndex++;
    }

    if (available === 'true') {
      sql += ` AND v.is_available = true`;
    } else if (available === 'false') {
      sql += ` AND v.is_available = false`;
    }

    sql += ` ORDER BY v.created_at DESC`;

    const result = await query(sql, queryParams);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(result.rows)
    };
  } catch (error) {
    console.error('Error fetching vehicles:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ detail: 'Failed to fetch vehicles: ' + error.message })
    };
  }
};
