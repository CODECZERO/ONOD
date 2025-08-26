#!/usr/bin/env python3
import requests
import json
import sys

def test_document_storage():
    """Test the Aptos document storage API endpoint"""
    
    # API endpoint
    url = "http://127.0.0.1:4008/api/v1/vendore/trainIssue"
    
    # Test data
    test_data = {
        "issuer": "af7f267620730968548a6b63a492c557afd8af3add4642fac61af602d6675350",
        "privateKey": "ed25519-priv-0xd6c7fe588e241fbb7280ecd983c20be20322ee5cda810c491de966241b1a7695",
        "receiver": "d0c74dbc95ce6eb201b4b0be7391a96d7f5be95ef94cef849b5ff5cfd3b9e6aa",
        "docType": "EducationCertificate",
        "docId": "CERT-2025-0001",
        "metaData": {
            "info": "Issued by GH Raisoni College"
        },
        "chain": []
    }
    
    # Headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    print("Testing Aptos Document Storage API")
    print("=" * 50)
    print(f"URL: {url}")
    print(f"Method: POST")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    print("=" * 50)
    
    try:
        print("Sending request... Please wait for blockchain transaction to complete.")
        print("This may take 10-30 seconds...")
        
        # Make the POST request with a longer timeout for blockchain operations
        response = requests.post(url, json=test_data, headers=headers, timeout=60)
        
        # Print response details
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print("=" * 50)
        
        # Try to parse the JSON response
        try:
            response_json = response.json()
            print("Response JSON:")
            print(json.dumps(response_json, indent=2))
        except json.JSONDecodeError:
            print("Response Text:")
            print(response.text)
        
        print("=" * 50)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("✅ SUCCESS: Request completed successfully")
            return True
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            return False
             
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to the server")
        print("Make sure the server is running on http://127.0.0.1:4008")
        return False
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request timed out after 60 seconds")
        print("The blockchain transaction is taking longer than expected")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Request failed - {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: Unexpected error - {e}")
        return False

def test_with_different_data():
    """Test with multiple different document IDs"""
    
    base_url = "http://127.0.0.1:4008/api/v1/vendore/trainIssue"
    
    test_cases = [
        {
            "name": "Test Case 1 - Original",
            "data": {
                "issuer": "af7f267620730968548a6b63a492c557afd8af3add4642fac61af602d6675350",
                "privateKey": "ed25519-priv-0xd6c7fe588e241fbb7280ecd983c20be20322ee5cda810c491de966241b1a7695",
                "receiver": "d0c74dbc95ce6eb201b4b0be7391a96d7f5be95ef94cef849b5ff5cfd3b9e6aa",
                "docType": "EducationCertificate",
                "docId": "CERT-2025-0001",
                "metaData": {
                    "info": "Issued by GH Raisoni College"
                },
                "chain": []
            }
        },
        {
            "name": "Test Case 2 - Different Doc ID",
            "data": {
                "issuer": "af7f267620730968548a6b63a492c557afd8af3add4642fac61af602d6675350",
                "privateKey": "ed25519-priv-0xd6c7fe588e241fbb7280ecd983c20be20322ee5cda810c491de966241b1a7695",
                "receiver": "d0c74dbc95ce6eb201b4b0be7391a96d7f5be95ef94cef849b5ff5cfd3b9e6aa",
                "docType": "EducationCertificate",
                "docId": "CERT-2025-0002",
                "metaData": {
                    "info": "Issued by GH Raisoni College - Second Certificate"
                },
                "chain": []
            }
        },
        {
            "name": "Test Case 3 - Another Doc ID",
            "data": {
                "issuer": "af7f267620730968548a6b63a492c557afd8af3add4642fac61af602d6675350",
                "privateKey": "ed25519-priv-0xd6c7fe588e241fbb7280ecd983c20be20322ee5cda810c491de966241b1a7695",
                "receiver": "d0c74dbc95ce6eb201b4b0be7391a96d7f5be95ef94cef849b5ff5cfd3b9e6aa",
                "docType": "InternshipCertificate",
                "docId": "INT-2025-0001",
                "metaData": {
                    "info": "Issued by XYZ Company for a summer internship"
                },
                "chain": []
            }
        },
        {
            "name": "Test Case 4 - Final Doc ID",
            "data": {
                "issuer": "af7f267620730968548a6b63a492c557afd8af3add4642fac61af602d6675350",
                "privateKey": "ed25519-priv-0xd6c7fe588e241fbb7280ecd983c20be20322ee5cda810c491de966241b1a7695",
                "receiver": "d0c74dbc95ce6eb201b4b0be7391a96d7f5be95ef94cef849b5ff5cfd3b9e6aa",
                "docType": "ParticipationCertificate",
                "docId": "PART-2025-0001",
                "metaData": {
                    "info": "Issued for participation in a hackathon"
                },
                "chain": []
            }
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*20} {test_case['name']} {'='*20}")
        
        try:
            print("Sending request... Please wait for blockchain transaction to complete.")
            print("This may take 10-30 seconds...")
            
            response = requests.post(
                base_url, 
                json=test_case['data'], 
                headers={'Content-Type': 'application/json'},
                timeout=60
            )
            
            result = {
                'test_name': test_case['name'],
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'doc_id': test_case['data']['docId']
            }
            
            if response.status_code == 200:
                print(f"✅ SUCCESS: {test_case['name']}")
                try:
                    response_data = response.json()
                    result['response'] = response_data
                    print(f"Transaction Hash: {response_data.get('hash', 'N/A')}")
                except:
                    result['response'] = response.text
            else:
                print(f"❌ FAILED: {test_case['name']} - Status: {response.status_code}")
                result['error'] = response.text
                
            results.append(result)
            
        except Exception as e:
            print(f"❌ ERROR in {test_case['name']}: {e}")
            results.append({
                'test_name': test_case['name'],
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    successful = sum(1 for r in results if r.get('success', False))
    total = len(results)
    print(f"Successful: {successful}/{total}")
    
    for result in results:
        status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
        print(f"{status} - {result['test_name']}")
    
    return results

if __name__ == "__main__":
    print("Aptos Document Storage API Tester")
    print("=" * 50)
    
    # Run the initial test
    single_success = test_document_storage()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--multiple":
        print("\n" + "=" * 50)
        print("Running Multiple Test Cases...")
        test_with_different_data()
    
    elif single_success:
        print("\n" + "=" * 50)
        print("Single test passed! Run with --multiple flag to test multiple cases:")
        print("python test_script.py --multiple")