// Register endpoint
const { query } = require('./db');
const { hashPassword, generateToken } = require('./auth-utils');

exports.handler = async (event) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle preflight
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  // Only allow POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { full_name, email, phone, password, user_type, location } = JSON.parse(event.body);

    // Validation
    if (!full_name || !email || !phone || !password) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ detail: 'Missing required fields' })
      };
    }

    // Password validation
    if (password.length < 8 || !/[A-Z]/.test(password) || !/\d/.test(password)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          detail: 'Password must be at least 8 characters with 1 uppercase letter and 1 digit'
        })
      };
    }

    // Check if user exists
    const existingUser = await query(
      'SELECT id FROM users WHERE email = $1',
      [email]
    );

    if (existingUser.rows.length > 0) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ detail: 'Email already registered' })
      };
    }

    // Hash password
    const hashedPassword = await hashPassword(password);

    // Insert user
    const result = await query(
      `INSERT INTO users (full_name, email, phone, password_hash, user_type, location, role, is_active, is_verified)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
       RETURNING id, full_name, email, phone, user_type, role, created_at`,
      [
        full_name,
        email,
        phone,
        hashedPassword,
        user_type || 'individual',
        JSON.stringify(location || {}),
        'customer',
        true,
        false
      ]
    );

    const user = result.rows[0];

    // Generate token
    const token = generateToken(user.id, user.email, user.role);

    return {
      statusCode: 201,
      headers,
      body: JSON.stringify({
        access_token: token,
        token_type: 'bearer',
        user: {
          id: user.id,
          full_name: user.full_name,
          email: user.email,
          phone: user.phone,
          user_type: user.user_type,
          role: user.role,
          created_at: user.created_at
        }
      })
    };
  } catch (error) {
    console.error('Registration error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ detail: 'Registration failed: ' + error.message })
    };
  }
};
