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

import axios from 'axios'

app.post('/chat', async (req, res) => {
  const { session_id, message } = req.body

  try {

    // Save user message
    await supabase.from('messages').insert([
      {
        session_id: session_id,
        sender: 'patient',
        message: message
      }
    ])

    // Fetch entire conversation from DB
    const { data: messages, error } = await supabase
      .from('messages')
      .select('*')
      .eq('session_id', session_id)
      .order('created_at', { ascending: true })

    if (error) throw error

    // Format conversation for AI
    const conversation = messages.map(msg => ({
      role: msg.sender === 'patient' ? 'user' : 'assistant',
      content: msg.message
    }))

    // Send full conversation to Python AI
    const aiResponse = await axios.post('http://127.0.0.1:8000/chat', {
      conversation: conversation
    })

    const reply = aiResponse.data.reply

    // Save AI reply
    await supabase.from('messages').insert([
      {
        session_id: session_id,
        sender: 'ai',
        message: reply
      }
    ])

    // Return reply
    res.json({ reply })

  } catch (err) {
    console.error(err)
    res.status(500).json({ error: "Chat failed" })
  }
})


app.post('/start-session', async (req, res) => {
  const { patient_id } = req.body

  const { data, error } = await supabase
    .from('sessions')
    .insert([{ patient_id }])
    .select()

  if (error) {
    return res.status(400).json({ error: error.message })
  }

  res.json({ session: data[0] })
})

