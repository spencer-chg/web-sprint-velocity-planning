-- Sprint Velocity Planning Database Schema

-- Sprints table
CREATE TABLE sprints (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    sprint_id TEXT UNIQUE NOT NULL,
    sprint_name TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    sprint_days INTEGER DEFAULT 10,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Sprint assignments (who worked on what)
CREATE TABLE sprint_assignments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    sprint_id TEXT REFERENCES sprints(sprint_id) ON DELETE CASCADE,
    engineer_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    story_points DECIMAL(5,2) DEFAULT 0,
    pto_days DECIMAL(4,2) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Team assignments (current team for each dev)
CREATE TABLE team_assignments (
    engineer_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security but allow all operations (no auth)
ALTER TABLE sprints ENABLE ROW LEVEL SECURITY;
ALTER TABLE sprint_assignments ENABLE ROW LEVEL SECURITY;
ALTER TABLE team_assignments ENABLE ROW LEVEL SECURITY;

-- Policies for public access (since no login required)
CREATE POLICY "Allow all" ON sprints FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all" ON sprint_assignments FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all" ON team_assignments FOR ALL USING (true) WITH CHECK (true);

-- Insert default team assignments
INSERT INTO team_assignments (engineer_id, team_id) VALUES
    ('fredrik-svensson', 'team1'),
    ('fernando-fernandez', 'team1'),
    ('matthew-callison', 'team1'),
    ('cody-worthen', 'team1'),
    ('stephen-corry', 'team2'),
    ('tom-sharrock', 'team2'),
    ('brady-hession', 'team2'),
    ('jaime-virrueta', 'team2');
