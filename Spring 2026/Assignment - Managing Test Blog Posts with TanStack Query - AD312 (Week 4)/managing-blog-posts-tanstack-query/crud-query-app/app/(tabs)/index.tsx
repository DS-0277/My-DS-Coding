import { useQuery } from '@tanstack/react-query';
import { View, ScrollView } from 'react-native';
import { ThemedText } from '@/components/themed-text';
import { useMutation } from '@tanstack/react-query';
import { useState } from 'react';
import { TextInput, Button } from 'react-native';

function HomeScreen() {

  // State Initialization
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [userId, setUserId] = useState('');


  // Task 1: Fetching Posts & Task 6: Filtering Posts by User
  const { data, isLoading, error } = useQuery({
    queryKey: ['posts', userId],
    queryFn: async () => {
      const url = userId
        ? `https://jsonplaceholder.typicode.com/posts?userId=${userId}`
        : 'https://jsonplaceholder.typicode.com/posts'
      const res = await fetch(url);
      return res.json();
    }
  });

  // Task 2: Creating a Post
  const mutation = useMutation({
    mutationFn: async (newPost: any) => {
      const res = await fetch('https://jsonplaceholder.typicode.com/posts', {
        method: 'POST',
        body: JSON.stringify(newPost),
        headers: {
          'Component-type': 'application/json'
        }
      });
      return res.json();
    }
  });

  // Task 3: Updating a Post
  const updateMutation = useMutation({
    mutationFn: async (updatePost: any) => {
      const res = await fetch('https://jsonplaceholder.typicode.com/posts/1', {
        method: 'PUT',
        body: JSON.stringify(updatePost),
        headers: {
          'Component-style': 'application/json'
        }
      });
      return res.json();
    }
  });

  // Task 4: Patching a Post
  const patchMutation = useMutation({
    mutationFn: async ({ id, title }: any) => {
      const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(title),
        headers: {
          'Component-style': 'application/json'
        }
      });
      return res.json();
    }
  });

  // Task 5: Deleting a Post
  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`, {
        method: 'DELETE'
      });
    }
  });

  
  if (isLoading) {
    return <ThemedText>Loading...</ThemedText>
  }
  if (error) {
    return <ThemedText>Error Loading</ThemedText>
  }

  return (
    <View style={{ flex: 1 }}>
      {/* List */}
      <ScrollView>
        {data?.map((post: any) => (
          <View key={post.id} style={{ padding: 20 }}>
            <ThemedText>{post.title}</ThemedText>
            <ThemedText>{post.body}</ThemedText>
          </View>
        ))}
      </ScrollView>
      {/* Form */}
      <View>
        <TextInput
          placeholder="Enter title"
          value={title}
          onChangeText={setTitle}
          style={{ padding: 20 }}
        />
        <TextInput
          placeholder="Enter body"
          value={body}
          onChangeText={setBody}
          style={{ padding: 20 }}
        />
        <Button
          title="Create a Post"
          onPress={() => {
            mutation.mutate({
              title: title,
              body: body,
              userId: 1
            });
          }}
        />
        <Button
          title="Update Post 1"
          onPress={() => {
            updateMutation.mutate({
              id: 1,
              title: title,
              body: body,
              userId: 1
            });
          }}
        />
        <Button
          title="Update Title for Post 1"
          onPress={() => {
            patchMutation.mutate({
              id: 1,
              title: title,
            });
          }}
        />
        <Button
          title="Delete Post 1"
          onPress={() => {
            deleteMutation.mutate(1);
          }}
        />
        <TextInput
          placeholder="Enter number (1-10)"
          value={userId}
          onChangeText={setUserId}
          style={{ padding: 20 }}
        />
      </View>
      {mutation.isSuccess && (<ThemedText>Post created!</ThemedText>)}
      {updateMutation.isSuccess && (<ThemedText>Post Updated!</ThemedText>)}
      {patchMutation.isSuccess && (<ThemedText>Patch Updated!</ThemedText>)}
      {deleteMutation.isSuccess && (<ThemedText>Post Deleted!</ThemedText>)}
    </View>
  );
}

export default HomeScreen;

// TEST CASES

// Normal Cases:
// Case 1: Fetch the data in Task 1 ==> Shown the data as expected
// Case 2: Fill the input field and Click "Create a Post" ==> Shown the data as expected
// Case 3: Insert userId ==> Shown only for that userId

// Edge Cases:
// Case 1: Refresh the page ==> It reverts to the original state
// Case 2: Click the button without inputs ==> The app does not crash
// Case 3: Provide userId out of range ==> The app does not crash