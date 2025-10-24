// Create rental booking
const { query } = require('./db');
const { requireAuth } = require('./auth-utils');

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  // Check authentication
  const auth = requireAuth(event);
  if (!auth.authenticated) {
    return {
      statusCode: 401,
      headers,
      body: JSON.stringify({ detail: auth.error })
    };
  }

  try {
    const { vehicle_id, start_date, end_date, pickup_location, notes } = JSON.parse(event.body);

    if (!vehicle_id || !start_date || !end_date || !pickup_location) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ detail: 'Missing required fields' })
      };
    }

    // Check vehicle availability
    const vehicleResult = await query(
      'SELECT id, daily_rate, is_available FROM vehicles WHERE id = $1',
      [vehicle_id]
    );

    if (vehicleResult.rows.length === 0) {
      return {
        statusCode: 404,
        headers,
        body: JSON.stringify({ detail: 'Vehicle not found' })
      };
    }

    const vehicle = vehicleResult.rows[0];
    if (!vehicle.is_available) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ detail: 'Vehicle is not available' })
      };
    }

    // Calculate total cost
    const startDate = new Date(start_date);
    const endDate = new Date(end_date);
    const days = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));
    const totalCost = days * vehicle.daily_rate;

    // Create rental
    const result = await query(
      `INSERT INTO rentals (
        user_id, vehicle_id, start_date, end_date,
        total_cost, pickup_location, status, notes
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
      RETURNING id, user_id, vehicle_id, start_date, end_date,
                total_cost, pickup_location, status, created_at`,
      [
        auth.user.user_id,
        vehicle_id,
        start_date,
        end_date,
        totalCost,
        pickup_location,
        'pending',
        notes || null
      ]
    );

    // Mark vehicle as unavailable
    await query(
      'UPDATE vehicles SET is_available = false WHERE id = $1',
      [vehicle_id]
    );

    return {
      statusCode: 201,
      headers,
      body: JSON.stringify(result.rows[0])
    };
  } catch (error) {
    console.error('Error creating rental:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ detail: 'Failed to create rental: ' + error.message })
    };
  }
};
