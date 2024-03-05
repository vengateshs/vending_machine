## Vending Machine Service

### Notes
- Path to OpenAPI Specification: _"/docs/openapi_spec.yaml"_

- APIs are secured with Basic Authentication Scheme

- Service is containerized as Docker container

- Path to Postman Collection: _"/docs/postman_collection"_

### Assumptions

- Role of a user is immutable

- Deposits are retained after user unregistration

- Buy request will be successful only if the balance is sufficient to buy all the products requested. Partial purchase is not allowed.

### Steps to run the service

- Clone the repository

- Build the docker image from the root directory:
    - `docker build -t myimage .`

- Run a container based on your image:
    - `docker run -d --name mycontainer -p 80:80 myimage`


### Enhancements

- Store in-memory data (users, products, deposits) in a database

- More error and exception handling

## Test Cases

### Deposit

1. Deposit - Without Authorization header
    - Deposit a valid coin without the header
        - expect 401 error
2. Deposit - UnRegistered user / Valid coin
    - Deposit a valid coin with authorization header but user not registered
        - expect 401 error
3. Deposit - Registered user / Seller role / Valid coin
    - Register a user as Seller
    - Deposit a valid coin by the user
        - expect 403 error
4. Deposit - Registered user / Buyer role / Invalid coin
    - Register a user as Buyer
    - Deposit a invalid coin by the user
        - expect 400 error
5. Deposit - Registered user / Buyer role / Valid coin
    - Register a user as Buyer
    - Deposit a valid coin by the user
        - expect 200 with balance details

### Buy

1. Buy - Without Authorization header
    - Buy request without the authorization header
        - expect 401 error
2. Buy - UnRegistered user / Valid request body
    - Buy request with authorization header and valid body but user not registered
        - expect 401 error
3. Buy - Registered user / Seller role / Valid request body
    - Register a user as Seller
    - Buy request with valid request body by the user
        - expect 403 error
4. Buy - Registered user / Buyer role / Invalid productId in the request body
    - Register a user as Buyer
    - Buy request with invalid productId in the request body by the user
        - expect 400 error
5. Buy - Registered user / Buyer role / Valid productId in the request body / Without sufficient balance
    - Register a user as Buyer
    - Register a product 
    - Buy request for the registered product by the registered user
        - expect 400 error
6. Buy - Registered user / Buyer role / Valid productId in the request body / With sufficient deposit
    - Register a user as Buyer
    - Register a product 
    - Deposit sufficient coins for the purchase by the Buyer user
    - Buy request for the registered product by the registered user
        - expect 200 with purchase details

### Reset

1. Reset - Without Authorization header
    - Reset request without the authorization header
        - expect 401 error
2. Reset - UnRegistered user
    - Reset request with authorization header but user not registered
        - expect 401 error
3. Reset - Registered user / Seller role
    - Register a user as Seller
    - Reset request by the user
        - expect 403 error
4. Reset - Registered user / Buyer role / Without deposit
    - Register a user as Buyer
    - Reset request by the user
        - expect 200
5. Reset - Registered user / Buyer role / With deposit
    - Register a user as Buyer
    - Make some deposits by the Buyer user
    - Reset request by the user
        - expect 200
5. Reset - Registered user / Buyer role / With deposit / Buy / Reset
    - Register a user as Buyer
    - Register a product 
    - Deposit sufficient coins for the purchase by the Buyer user
    - Buy request for the registered product by the registered user
        - expect 200 with purchase details
    - Reset request by the user
        - expect 200
6. Reset - Registered user / Buyer role / With deposit / Reset / Buy
    - Register a user as Buyer
    - Register a product 
    - Deposit sufficient coins for the purchase by the Buyer user
    - Reset request by the user
        - expect 200
    - Buy request for the registered product by the registered user
        - expect 400 error
