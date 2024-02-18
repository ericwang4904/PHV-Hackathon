# PHV-Hackathon

# THIS IS A DEMO APP. DO NOT USE EXCEPT FOR DEVELOPMENT!
Limitations:
- NO SECURITY for admin section; anyone user can query the LLM or delete the question database.
- No flask production server
- Untested compatability for multiple network instances (should work though)
- Looks pretty dated in terms of UI

# Parts
Website UI:
1. LOW PRIORITY

Website Backend:
1. Asker and Answer Inputs
   1. Make it so you can't put in the same question over and over
   2. Don't want to Disincentvize the student, though
      1. Timer, less weight for more questions (1 question > 5 question over the same amount of time).
   3. "storing" questons
2. Filter for Questions
3. Return Final Questions - put a cap on this?
   1. Professor can see list of questions, 
   2. Professor can see NUMBER OF QUESTIONS IN CLUSTER

Model Backend:

1. Input - Jason
   1. List of questions
   2. arguments for model (like clustering distance?)
2. Vectorizing - Jason
   1. sentence transformers?
3. Clustering - Jason
   1. k-means or similar for automatic clustering
   2. What can't work:
      1. K-means (needs number of clusters to determine "intertia" of various sentences that differ from a mean)
      2. 
   3. What can work:
      1. Affinity Propagation (takes in a bunch of points, sees how relative they are all from each other with max and min until they can find a convergent cluster point. No need to input number of clusters and stuff, but time complexity is O(N^2T) where N is # of clusters, T is number of iterations) - Inputs are preference (how many exemplars: what questions are most related as central nodes in clusters), damping factors (determining responsibility and aviailabiliy messages).
         1. Responsibility: r(i,k) is how much sample k should be exemplar for i
         2. Availability: a(i,k) is how much sample i should choose k as exemplar
      2. 
4. AI model
   1. APIs
5. Output
   1. return list of questions