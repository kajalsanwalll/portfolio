// api/leetcode.js
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  
  const query = `query {
    matchedUser(username: "kajalsanwall") {
      profile { ranking }
      submitStats { acSubmissionNum { difficulty count } }
      userCalendar { streak submissionCalendar }
      badges { displayName }
    }
    userContestRanking(username: "kajalsanwall") {
      rating attendedContestsCount topPercentage
    }
  }`;

  const lcRes = await fetch('https://leetcode.com/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Referer': 'https://leetcode.com' },
    body: JSON.stringify({ query }),
  });

  const data = await lcRes.json();
  res.status(200).json(data);
}