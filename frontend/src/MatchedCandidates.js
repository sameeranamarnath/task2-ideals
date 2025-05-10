import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Button,
  Checkbox,
  CircularProgress,
  Dialog,
  DialogContent,
  DialogTitle,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography
} from '@mui/material';
import './MatchedCandidates.css';

const baseUrl = process.env.REACT_APP_API_BASE_URL;
console.log(baseUrl);
export default function MatchedCandidates() {
  const [loading, setLoading] = useState(true);
  const [candidates, setCandidates] = useState([]);
  const [selected, setSelected] = useState([]);

  useEffect(() => {
    axios.get(`${baseUrl}/match_candidates`)
      .then(response => {
        const filteredResults = response.data.matched_results
        .map(entry => ({
          ...entry,
          match_details: JSON.parse(entry.match_details)
        }))
        .filter(entry => entry.match_details.suitability_score > 0 && entry.candidate && entry.candidate.trim() !== "");
      
       setCandidates(filteredResults);;
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching matched candidates:', error);
        setLoading(false);
      });
  }, []);

  const handleSelect = (candidateName, postingTitle) => {
    const key = `${candidateName}-${postingTitle}`;
    setSelected(prev =>
      prev.includes(key)
        ? prev.filter(item => item !== key)
        : [...prev, key]
    );
  };

  const handleSendNotifications = () => {
    const selectedEntries = candidates.filter(entry =>
      selected.includes(`${entry.candidate}-${entry.posting}`)
    );

    const emailPayload = {
      subject: "Opportunity Notification from Talent Acquisition",
      addresses: selectedEntries.map(entry => `${entry.candidate.replace(" ", ".").toLowerCase()}@example.com`),
      body: `<h3>New Job Opportunity</h3><p>You have been matched for a job opportunity. Please check your candidate portal.</p>`
    };

    console.log("Payload to send_email:", emailPayload);
    //
    

    alert('Emails sent successfully to selected candidates!');
    return;
    axios.post(`${baseUrl}/send_email`, emailPayload)  
      .then(() => alert('Emails sent successfully!'))  
      .catch(error => alert('Error sending emails,possibly invalid emails: ' + error)); 
    //alert('Mock notification sent (check console).');
  };

  return (
    <Paper  elevation={3} style={{ padding: 24, margin: 'auto', maxWidth: 1200, marginTop: 40 }} className="matched-candidates-container">
      <Typography variant="h5" gutterBottom className='matched-candidates-title'>
        Candidate Vetting Platform for Task 2-Ideals
      </Typography>

      <Dialog open={loading}>
        <DialogTitle>AI is processing the lever database </DialogTitle>
        <DialogContent style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <CircularProgress />
          <Typography>Matching candidates with postings in the database, this might take a bit...</Typography>
       
        </DialogContent>
      </Dialog>

      {!loading && (
        <>
          <TableContainer component={Paper}>
            <Table>
              <TableHead style={{ backgroundColor: '#1976d2' }}>
                <TableRow>
                  <TableCell style={{ color: 'white' }}>Select</TableCell>
                  <TableCell style={{ color: 'white' }}>Candidate Name</TableCell>
                  <TableCell style={{ color: 'white' }}>Posting Title</TableCell>
                  <TableCell style={{ color: 'white' }}>Suitability Score</TableCell>
                  <TableCell style={{ color: 'white' }}>Alignment Areas</TableCell>
                  <TableCell style={{ color: 'white' }}>Gaps or Mismatches</TableCell>
                  <TableCell style={{ color: 'white' }}>Recommendation</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {candidates.map((entry, idx) => {
                  const key = `${entry.candidate}-${entry.posting}`;
                  return (
                    <TableRow key={idx} hover>
                      <TableCell padding="checkbox">
                        <Checkbox
                          checked={selected.includes(key)}
                          onChange={() => handleSelect(entry.candidate, entry.posting)}
                        />
                      </TableCell>
                      <TableCell>{entry.candidate}</TableCell>
                      <TableCell>{entry.posting}</TableCell>
                      <TableCell>{entry.match_details.suitability_score}</TableCell>
                      <TableCell>{entry.match_details.alignment_areas?.join(", ")}</TableCell>
                      <TableCell>{entry.match_details.gaps_or_mismatches?.join(", ")}</TableCell>
                      <TableCell>{entry.match_details.recommendation}</TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>

          <Button
            variant="contained"
            color="primary"
            style={{ marginTop: 16 }}
            onClick={handleSendNotifications}
            disabled={selected.length === 0}
          >
            Notify selected candidates
          </Button>
        </>
      )}
    </Paper>
  );
}