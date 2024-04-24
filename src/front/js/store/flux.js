const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			demo: [{title: "FIRST", background: "white", initial: "white"},
				     {title: "SECOND", background: "white", nitial: "white"}],
			message: null,
		},
		actions: {
			// Use getActions to call a function within a fuction
			exampleFunction: () => { getActions().changeColor(0, "green") },
			getMessage: async () => {
					const url = process.env.BACKEND_URL + "/api/hello";
					const options = {
						method: 'GET',
						headers: {
							'Content-Type': 'application/json'
						}
					}
					const response = await fetch(url, options);
					if (!response.ok) {
						console.log('Error: ', response.status, response.statusText)
						setStore({ message: `Error: ${response.status} ${response.statusText}` });
						return;  // Don't forget to return something, that is how the async resolves
					}
					const data = await response.json();
					setStore({ message: data.message });
					return 
			},
			changeColor: (index, color) => {
				const store = getStore();  // Get the store
				// We have to loop the entire demo array to look for the respective index and change its color
				const demo = store.demo.map((element, i) => {
					if (i === index) {
						element.background = color;
					};
					return element;
				});
				setStore({ demo: demo });  // Reset the global store
			}
		}
	};
};


export default getState;
