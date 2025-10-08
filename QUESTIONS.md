# Forensic Investigation Query Examples for Project Drishti

## 📋 Overview

This document contains 100 realistic forensic investigation queries that demonstrate Project Drishti's Hybrid Intelligence Architecture. These questions are designed to test both the Detective Tool (SQL) and Interrogator Tool (RAG), as well as cross-referencing capabilities.

---

## 🔍 Category 1: Basic Call Analysis (Detective - SQL)

### Call Patterns & Frequency

1. How many calls were made in total?
2. Show me all calls made after 10 PM
3. List all calls made between 11 PM and 5 AM
4. How many calls were made to unsaved numbers?
5. What is the total duration of all incoming calls?
6. Show me the top 10 most called numbers
7. How many outgoing calls lasted more than 30 minutes?
8. List all missed calls in chronological order
9. Show me calls made during working hours (9 AM - 5 PM)
10. How many calls were made on weekends?

### Call Duration Analysis

11. What is the average call duration for outgoing calls?
12. Show me all calls that lasted less than 5 seconds
13. List the longest 5 calls with their timestamps
14. How many calls lasted exactly 0 seconds (failed connections)?
15. What is the total talk time for the past week?

### Number-Specific Queries

16. Show me all calls to and from +91-9876543210
17. How many different numbers were contacted?
18. List all numbers that were called more than 10 times
19. Show me numbers that received calls but never called back
20. Which number has the highest cumulative call duration?

---

## 💬 Category 2: Communication Content Analysis (Interrogator - RAG)

### Chat & Message Analysis

21. What did the suspects discuss in their WhatsApp chats?
22. Summarize the key points from the investigation notes
23. What suspicious activities are mentioned in the device info?
24. Describe the conversation patterns in the chat history
25. What locations are mentioned in the text messages?
26. What are the main topics discussed in the encrypted chats?
27. Are there any mentions of illegal activities?
28. What code words or suspicious language patterns are present?
29. Describe the tone and urgency in recent messages
30. What plans or meetings are discussed in the chats?

### Document & Note Analysis

31. Summarize the findings from forensic examiner notes
32. What evidence is documented in the device analysis report?
33. Are there any contradictions in the suspect's statements?
34. What technical details are mentioned about the device?
35. What apps were found to contain incriminating evidence?
36. Describe the digital footprint patterns
37. What metadata is significant in the recovered files?
38. Are there deleted messages that were recovered?
39. What time-sensitive information is in the notes?
40. What external contacts or organizations are mentioned?

---

## 📊 Category 3: SMS & Message Patterns (Detective - SQL)

### SMS Analysis

41. Show me all SMS messages containing the word "money"
42. How many messages were sent after midnight?
43. List all messages exchanged with contact "Rahul"
44. Show me the frequency of SMS per day for the last month
45. How many messages contain phone numbers in the text?
46. List all SMS containing currency symbols (₹, $, €)
47. Show me messages sent during the time of the incident
48. How many group messages were sent?
49. List all SMS with attachments
50. Show me the distribution of incoming vs outgoing messages

---

## 💰 Category 4: Financial Transaction Analysis (Detective - SQL)

### Transaction Patterns

51. Show me all transactions over ₹1 lakh
52. List all transactions made at night (10 PM - 6 AM)
53. What is the total amount transferred in the last 7 days?
54. Show me all transactions to account number XXXX1234
55. How many transactions were made to the same beneficiary?
56. List all failed or declined transactions
57. Show me the daily transaction volume trend
58. What is the average transaction amount?
59. List all transactions flagged as suspicious
60. Show me transactions made from unusual locations

### Payment Method Analysis

61. How many UPI transactions were made?
62. Show me all cash withdrawals over ₹50,000
63. List all credit card transactions
64. How many international transactions occurred?
65. Show me all transactions with beneficiary name "Unknown"

---

## 🔗 Category 5: Cross-Reference & Link Analysis (Both Tools)

### Communication-Transaction Correlation

66. Find all communications that mention people who made suspicious transactions
67. Show me calls made within 1 hour before large financial transfers
68. Are there WhatsApp messages discussing the transactions over ₹5 lakh?
69. Cross-reference phone numbers in SMS with transaction beneficiaries
70. Show me the timeline of events linking calls, messages, and transactions
71. Find conversations that occurred during the time of fraudulent activities
72. Which contacts discussed meeting at locations where transactions occurred?
73. Are there messages about transactions that don't appear in the bank records?
74. Show me communication patterns before and after suspicious payments
75. Link the device location history with transaction timestamps

### Contact Network Analysis

76. Show me all contacts that communicated with both the primary and secondary suspects
77. Find common contacts between different chat groups
78. Which phone numbers appear in both call logs and message content?
79. Identify intermediaries who connected multiple suspects
80. Show me contacts who were added during the investigation period

---

## 📍 Category 6: Location & Device Analysis (Interrogator - RAG + Detective - SQL)

### Location Intelligence

81. What locations does the suspect frequently visit according to GPS data?
82. Show me the location history during the time of the incident
83. Are there any mentions of meeting places in the chat history?
84. Cross-reference location data with call tower information
85. What addresses are mentioned in messages and notes?
86. Show me movements between 2 AM and 5 AM
87. Were there any international travels recorded?
88. What suspicious location patterns are evident?
89. Compare stated locations in messages with actual GPS coordinates
90. Show me location clusters indicating frequent meeting spots

---

## 📱 Category 7: App Usage & Browser History (Detective - SQL)

### Digital Behavior Analysis

91. Show me all apps used during late-night hours
92. What websites were visited related to cryptocurrency?
93. List all apps installed in the last 30 days
94. Show me browser history for banking websites
95. How much time was spent on social media apps?
96. List all encrypted messaging apps found on the device
97. Show me app usage during the time window of interest
98. What dark web or Tor browser activity was detected?
99. List all apps that access location services
100. Show me the most frequently used apps

---

## 📈 Category 8: Visualization & Reporting Queries

### Graph & Chart Generation

101. Create a timeline visualization of all communications and transactions
102. Show me a bar chart of call frequency by hour of day
103. Generate a network graph of all contacts and their connections
104. Visualize the transaction amounts over time as a line graph
105. Create a heat map of SMS activity by day of week
106. Show me a pie chart of call types (incoming, outgoing, missed)
107. Generate a scatter plot of transaction amounts vs. time
108. Create a geographical map of location visits
109. Visualize app usage patterns as a stacked area chart
110. Show me a correlation matrix between communication frequency and transaction amounts

### Trend Analysis

111. Show me the trend of communication frequency over the investigation period
112. Are transaction amounts increasing or decreasing over time?
113. Visualize the relationship between call duration and time of day
114. Show me seasonal patterns in communication behavior
115. Generate a moving average chart of daily transaction volumes

---

## 🔎 Category 9: Advanced Forensic Queries (Hybrid - Both Tools)

### Evidence Discovery

116. Find all evidence pointing to premeditation of the crime
117. What digital artifacts indicate knowledge of being under surveillance?
118. Show me attempts to delete or hide evidence
119. Are there any data recovery indicators in the forensic report?
120. What EXIF metadata from photos reveals about locations and timestamps?
121. Find discrepancies between stated activities and actual digital evidence
122. What patterns indicate the use of burner phones or alternate devices?
123. Show me evidence of coordination between multiple suspects
124. Are there indicators of technical sophistication in hiding activities?
125. What forensic timestamps don't align with suspect's alibi?

### Pattern Recognition

126. Identify unusual spikes in communication or financial activity
127. Show me behavioral changes before and after the incident
128. What patterns suggest involvement of organized crime?
129. Are there communication blackout periods that correlate with criminal activities?
130. Find patterns of test transactions before large fraudulent transfers

---

## 🚨 Category 10: Incident-Specific Analysis

### Timeline Reconstruction

131. Create a complete timeline of events for [specific date]
132. What was the suspect doing between 2 PM and 4 PM on [date]?
133. Show me all digital activities in the 24 hours before the incident
134. Reconstruct the sequence of communications leading to the transaction
135. What evidence exists for the suspect's whereabouts during the crime window?

### Motive & Intent Analysis

136. What financial pressures are evident from the transaction history?
137. Are there communications indicating planning or conspiracy?
138. Show me evidence of motive in messages and notes
139. What discussions about money problems appear in the chats?
140. Are there threats or coercion indicators in the messages?

---

## 🧩 Category 11: Anomaly Detection

### Suspicious Behavior Identification

141. Show me all activities that deviate from the suspect's normal patterns
142. What unusual contact additions occurred during the investigation period?
143. Are there sudden changes in communication frequency?
144. Show me transactions that are outliers compared to normal spending
145. What late-night activities are inconsistent with suspect's routine?
146. Find contacts that only appear during suspicious time periods
147. Show me communication patterns that suddenly stopped
148. What apps were used only once or twice but contain significant data?
149. Are there gaps in location data suggesting GPS manipulation?
150. Show me contacts who were communicated with intensely for short periods

---

## 📝 Category 12: Report Generation Queries

### Comprehensive Analysis

151. Generate a complete summary of all suspicious activities
152. Create an executive summary of the key evidence findings
153. Summarize all communications related to financial transactions
154. Generate a report of all contacts and their risk levels
155. Create a comprehensive timeline report with all evidence types
156. Summarize technical forensic findings from device analysis
157. Generate a network analysis report of all involved parties
158. Create a financial summary highlighting suspicious patterns
159. Generate a behavioral analysis report of the primary suspect
160. Summarize all evidence supporting the prosecution case

---

## 🎯 Category 13: Specific Evidence Validation

### Verifying Leads

161. Verify if phone number +91-XXXXXXXXXX appears in any communication
162. Check if "Hawala" or similar terms are mentioned anywhere
163. Validate if the suspect communicated with known criminals
164. Verify the authenticity of location claims made in messages
165. Check if there are communications during times suspect claimed to be sleeping
166. Validate if transaction descriptions match chat conversations
167. Verify if contact names match transaction beneficiary names
168. Check consistency between SMS timestamps and call log timestamps
169. Validate if deleted messages were actually about innocent topics
170. Verify if the suspect's version of events matches digital evidence

---

## 🔐 Category 14: Security & Encryption Analysis (Interrogator - RAG)

### Privacy & Concealment

171. What encryption methods were used in the communications?
172. Are there any mentions of VPN or proxy usage?
173. What attempts to hide identity are evident?
174. Are there discussions about using encrypted apps?
175. What anonymous payment methods are mentioned?
176. Are there references to cryptocurrency transactions?
177. What security-conscious behavior is evident in the chats?
178. Are there mentions of burner phones or temporary SIM cards?
179. What discussions about avoiding surveillance appear?
180. Are there coded messages or cipher usage indicators?

---

## 📞 Category 15: Contact Analysis (Both Tools)

### Relationship Mapping

181. Who are the most frequently contacted people?
182. Show me contacts that only communicated during late hours
183. What is the relationship network of the primary suspect?
184. Find contacts who were introduced by other suspects
185. Show me contacts with no saved name but high call frequency
186. What contacts appear in multiple case files?
187. Show me foreign numbers in the contact list
188. Which contacts were blocked or deleted?
189. What contacts have matching names in different chat apps?
190. Show me contacts added just before suspicious activities

---

## 🌐 Category 16: Internet & Social Media Activity (Detective - SQL)

### Online Behavior

191. Show me all Google searches related to money laundering
192. What social media platforms were most used?
193. List all YouTube videos watched related to fraud
194. Show me all online purchases made during the investigation period
195. What job posting or freelance sites were visited?
196. Show me all email addresses found in browser history
197. List all file downloads in the past 30 days
198. What cloud storage services were accessed?
199. Show me all login timestamps for various accounts
200. What forums or discussion boards were visited?

---

## 💡 Category 17: Intelligent Summarization (Interrogator - RAG)

### High-Level Analysis

201. What is the most incriminating piece of evidence?
202. Summarize the overall case narrative based on all evidence
203. What are the top 5 red flags in this investigation?
204. Describe the suspect's digital behavior profile
205. What evidence contradicts the suspect's statement?
206. Summarize the financial crime methodology used
207. What are the key takeaways for the investigation team?
208. Describe the level of sophistication in the criminal activity
209. What recommendations would you make for further investigation?
210. Summarize the strength of evidence for prosecution

---

## 🔬 Category 18: Technical Forensics (Both Tools)

### Device & Technical Details

211. What device information indicates tampering?
212. Show me factory reset attempts or data wiping activities
213. What rooting or jailbreaking evidence exists?
214. List all installed forensic detection apps
215. What anti-forensic tools were found on the device?
216. Show me system logs indicating suspicious activities
217. What apps have permission to delete SMS or call logs?
218. Are there signs of device cloning or SIM swapping?
219. What developer options or debug modes were enabled?
220. Show me evidence of multiple user accounts on the device

---

## 📅 Category 19: Time-Based Analysis (Detective - SQL)

### Temporal Patterns

221. Show me all activities on Sundays
222. What happens consistently every Tuesday at 3 PM?
223. Show me monthly patterns in transaction behavior
224. List all activities between Christmas and New Year
225. Show me the busiest day of the week for communications
226. What patterns occur on the 1st of every month?
227. Show me activities during public holidays
228. What time of day has the highest transaction volume?
229. Show me seasonal variations in behavior
230. List all activities during typical business hours vs. after hours

---

## 🎭 Category 20: Behavioral Profiling (Hybrid Analysis)

### Psychological & Behavioral Insights

231. What does the communication style reveal about the suspect?
232. Are there indicators of stress or panic in message timing?
233. What behavioral changes occurred after the incident?
234. Show me evidence of deliberate deception
235. What patterns suggest multiple people using the same device?
236. Are there indicators of substance abuse in communication patterns?
237. What evidence suggests involvement of family members?
238. Show me behaviors consistent with insider knowledge
239. What patterns indicate the suspect's technical competence level?
240. Are there signs of remorse or lack thereof in communications?

---

## 📊 Category 21: Statistical Analysis (Detective - SQL)

### Quantitative Metrics

241. What is the standard deviation in transaction amounts?
242. Calculate the correlation between call frequency and transaction volumes
243. Show me percentile rankings for transaction amounts
244. What is the median call duration?
245. Calculate the variance in daily communication frequency
246. Show me z-scores for outlier transactions
247. What is the mode for most common transaction amount?
248. Calculate the rolling 7-day average of communications
249. Show me quartile distribution of call durations
250. What is the coefficient of variation in spending patterns?

---

## 🏆 Category 22: Priority & Urgency Queries

### High-Priority Investigation Needs

251. What evidence needs immediate follow-up?
252. Show me the most time-sensitive leads
253. What communications indicate imminent criminal activity?
254. List evidence with approaching statute of limitations
255. What witnesses need to be interviewed urgently?
256. Show me evidence of ongoing criminal enterprise
257. What assets need immediate seizure?
258. Are there indicators of flight risk?
259. What evidence suggests destruction of additional evidence?
260. Show me contacts that should be placed under surveillance

---

## 🔄 Category 23: Cross-Case Analysis

### Multi-Case Investigation

261. Find similarities between this case and Case #12345
262. Show me contacts that appear in multiple investigations
263. What patterns are consistent across related cases?
264. Find common modus operandi indicators
265. Show me overlapping phone numbers across cases
266. What locations appear in multiple case files?
267. Are there shared cryptocurrency wallet addresses?
268. Find common app usage across suspects in related cases
269. Show me transaction patterns similar to previous cases
270. What evidence links this case to organized crime networks?

---

## 📱 Category 24: App-Specific Analysis (Both Tools)

### Application Deep Dive

271. Show me all WhatsApp group memberships
272. What Telegram channels was the suspect subscribed to?
273. List all Instagram messages with deleted content indicators
274. Show me Snapchat activity timestamps
275. What TikTok videos were shared related to money
276. Show me LinkedIn connections and job searches
277. What dating app communications are relevant?
278. Show me gaming app in-app purchases
279. What food delivery and ride-sharing app usage patterns exist?
280. List all cryptocurrency wallet app activities

---

## 🎨 Category 25: Multimedia Evidence (Interrogator - RAG)

### Photo, Video & Audio Analysis

281. What locations are revealed by photo EXIF data?
282. Describe the content of recovered videos
283. What audio recordings contain incriminating conversations?
284. What photos show the suspect with other persons of interest?
285. Describe memes or images shared that relate to criminal activity
286. What screenshots of banking apps were found?
287. What videos show the suspect at crime scene locations?
288. Describe voice notes discussing illegal activities
289. What photos were taken and immediately deleted?
290. What multimedia evidence contradicts alibis?

---

## 🎯 Category 26: Hypothesis Testing

### Investigation Validation

291. Does the evidence support the theory that the suspect acted alone?
292. Is there proof of the suspect being at [location] on [date]?
293. Can we prove the suspect had knowledge of the crime?
294. Does the digital evidence corroborate witness testimony?
295. Is there evidence of the alleged co-conspirator's involvement?
296. Can we establish means, motive, and opportunity?
297. Does the evidence refute the suspect's alibi?
298. Is there proof of intent to commit fraud?
299. Can we trace the flow of stolen money?
300. Does the evidence establish beyond reasonable doubt?

---

## 🔔 Usage Guidelines

### How to Use These Questions:

1. **Start Simple**: Begin with basic queries (Category 1-2) to understand the data
2. **Progressive Complexity**: Move to cross-referencing queries (Category 5) as you understand patterns
3. **Visualization**: Use Category 8 questions to create exportable charts for reports
4. **Case Building**: Use Categories 9-10 for building the prosecution case
5. **Final Analysis**: Use Categories 17 & 20 for comprehensive insights

### Query Best Practices:

✅ **DO:**
- Be specific with dates, times, and amounts
- Use exact phone numbers or contact names when known
- Ask for visualizations to spot patterns
- Request cross-references between different data types
- Ask for summaries after detailed queries

❌ **DON'T:**
- Ask vague questions without context
- Query sensitive data without proper authorization
- Assume conclusions - ask the system to find evidence
- Ignore timezone considerations in timestamps
- Forget to export visualizations for court documentation

---

## 📈 Expected Output Examples

### Detective Tool (SQL) Example:
**Query**: "Show me all transactions over ₹1 lakh"
**Output**:
- SQL query generated
- Table with: Date, Amount, Beneficiary, Method, Status
- Count: 15 transactions
- Visualization: Bar chart of amounts

### Interrogator Tool (RAG) Example:
**Query**: "What did the suspects discuss in WhatsApp?"
**Output**:
- Summary of key discussion points
- Identified topics: money transfer, meeting locations, code words
- Source citations with relevance scores
- Key quotes with timestamps

### Hybrid Analysis Example:
**Query**: "Find calls made within 1 hour before large transactions"
**Output**:
- Cross-referenced data from both tools
- Timeline showing calls → transactions
- Link analysis showing phone numbers mentioned in chats that match transaction beneficiaries
- Network visualization

---

## 🔐 Legal & Ethical Considerations

**⚠️ Important Reminders:**

1. **Authorization**: Ensure proper legal authorization before querying sensitive data
2. **Chain of Custody**: Document all queries for court evidence admissibility
3. **Privacy**: Respect privacy laws even during investigations
4. **Bias**: Be aware that AI analysis should supplement, not replace, human judgment
5. **Verification**: Always verify AI-generated insights with original data
6. **Documentation**: Export and archive query results for case files
7. **Access Control**: Restrict access to investigation data to authorized personnel only

---

## 📚 Additional Resources

- **README.md**: Complete system documentation
- **TROUBLESHOOTING.md**: Common issues and solutions
- **ARCHITECTURE.md**: Technical deep dive
- **IMPLEMENTATION_SUMMARY.md**: Feature checklist

---

**Document Version**: 1.0  
**Last Updated**: October 7, 2025  
**Total Questions**: 300  
**Author**: Project Drishti Team  
**Classification**: For Authorized Law Enforcement Use Only

---

🔍 **Project Drishti** - *Bringing Insight to Forensic Investigations*
