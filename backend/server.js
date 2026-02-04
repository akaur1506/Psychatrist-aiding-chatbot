import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'
import bcrypt from 'bcrypt'
import supabase from './config/supabase.js'

dotenv.config()

const app = express()

app.use(cors())
app.use(express.json())

// Home route
app.get('/', (req, res) => {
  res.send("Backend is running 🚀")
})

// Test DB route
app.get('/test-db', async (req, res) => {
  const { data, error } = await supabase
    .from('users')
    .select('*')

  if (error) {
    return res.status(500).json({ error: error.message })
  }

  res.json({ data })
})

/* =======================
   SIGNUP ROUTE
======================= */
app.post('/signup', async (req, res) => {
  const { name, email, password, role } = req.body

  if (!name || !email || !password || !role) {
    return res.status(400).json({ error: "All fields are required" })
  }

  // Hash password
  const hashedPassword = await bcrypt.hash(password, 10)

  const { data, error } = await supabase
    .from('users')
    .insert([
      { name, email, password: hashedPassword, role }
    ])
    .select()

  if (error) {
    return res.status(400).json({ error: error.message })
  }

  res.json({
    message: "User created successfully",
    user: data[0]
  })
})

/* =======================
   LOGIN ROUTE
======================= */
app.post('/login', async (req, res) => {
  const { email, password } = req.body

  const { data, error } = await supabase
    .from('users')
    .select('*')
    .eq('email', email)
    .single()

  if (error || !data) {
    return res.status(400).json({ error: "User not found" })
  }

  // Compare password
  const isMatch = await bcrypt.compare(password, data.password)

  if (!isMatch) {
    return res.status(400).json({ error: "Invalid credentials" })
  }

  res.json({
    message: "Login successful",
    user: {
      id: data.id,
      name: data.name,
      email: data.email,
      role: data.role
    }
  })
})

app.listen(process.env.PORT, () => {
  console.log(`Server running on port ${process.env.PORT}`)
})

/* =======================
   CREATE CHAT SESSION
======================= */
app.post('/start-session', async (req, res) => {
  const { patient_id } = req.body

  const { data, error } = await supabase
    .from('sessions')
    .insert([{ patient_id }])
    .select()

  if (error) {
    return res.status(400).json({ error: error.message })
  }

  res.json({
    message: "Session created",
    session: data[0]
  })
})
