**Hands-on Assignment - The StreamFlix Extra Features Challenges - AD350 (Week 6)**


**1. Objective:** In the previous weeks, we treated movies as rigid rows. But in the real world, a documentary has different data points (like "Interviewees") than an animated film (like "Voice Cast") or a 4K blockbuster (like "HDR format"). We’re going to use JSONB to turn our movies table into a hybrid powerhouse. Our marketing team wants to store "Extra Details" for movies, but they don't want to keep asking the Database Admins to add new columns every time they have a new piece of info. We’re going to give them a JSONB "Details" column where they can store whatever they want.

**2. Diagrams or Flowcharts:** Two images describing the assignment are attached herewith.

**3. The "Lightbulb" Moment:** Using one JSONB column is better for 'Extra Details' than creating 5 separate standard columns for things like 'Studio', 'Resolution', and 'Cast' because this approach avoids having rows full of NULL values and enables any data insertion without requiring modification of data schema every time.

**4. YouTube Link:** The explanation is provided via the youtube link as follows: https://youtu.be/5KjYUfRO5cw
