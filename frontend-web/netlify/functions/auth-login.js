// Login endpoint
const { query } = require('./db');
const { verifyPassword, generateToken } = require('./auth-utils');

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

  try {
    const { email, password } = JSON.parse(event.body);

    if (!email || !password) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ detail: 'Email and password required' })
      };
    }

    // Get user
    const result = await query(
      `SELECT id, full_name, email, phone, password_hash, user_type, role, is_active, is_verified
       FROM users WHERE email = $1`,
      [email]
    );

    if (result.rows.length === 0) {
      return {
        statusCode: 401,
        headers,
        body: JSON.stringify({ detail: 'Invalid credentials' })
      };
    }

    const user = result.rows[0];

    // Check if active
    if (!user.is_active) {
      return {
        statusCode: 403,
        headers,
        body: JSON.stringify({ detail: 'Account is inactive' })
      };
    }

    // Verify password
    const isValid = await verifyPassword(password, user.password_hash);
    if (!isValid) {
      return {
        statusCode: 401,
        headers,
        body: JSON.stringify({ detail: 'Invalid credentials' })
      };
    }

    // Generate token
    const token = generateToken(user.id, user.email, user.role);

    // Update last login
    await query(
      'UPDATE users SET last_login = NOW() WHERE id = $1',
      [user.id]
    );

    return {
      statusCode: 200,
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
          is_verified: user.is_verified
        }
      })
    };
  } catch (error) {
    console.error('Login error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ detail: 'Login failed: ' + error.message })
    };
  }
};
